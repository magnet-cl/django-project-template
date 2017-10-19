from compressor.exceptions import FilterError
from compressor.filters import CompilerFilter
from django.core.files.temp import NamedTemporaryFile
from django.utils.encoding import smart_text
import io
import os
import subprocess
from platform import system

if system() != "Windows":
    try:
        from shlex import quote as shell_quote  # Python 3
    except ImportError:
        from pipes import quote as shell_quote  # Python 2
else:
    from subprocess import list2cmdline

    def shell_quote(s):
        # shlex.quote/pipes.quote is not compatible with Windows
        return list2cmdline([s])


class PugCompilerFilter(CompilerFilter):
    binary = './node_modules/pug-cli/index.js'
    args = '-c -D'
    command = "{binary} {infile} {args} -o {outfile}"

    options = (
        ("binary", binary),
        ("args", args),
    )

    def input(self, **kwargs):

        encoding = self.default_encoding
        options = dict(self.options)

        relative_path = self.filename.split('static/templates/')[1][:-4]

        if self.infile is None and "{infile}" in self.command:
            # we use source file directly, which may be encoded using
            # something different than utf8. If that's the case file will
            # be included with charset="something" html attribute and
            # charset will be available as filter's charset attribute
            encoding = self.charset  # or self.default_encoding
            self.infile = open(self.filename)
            options["infile"] = self.filename

        basename = os.path.basename(self.filename)[:-3]

        if "{outfile}" in self.command and "outfile" not in options:
            # create temporary output file if needed
            ext = self.type and ".%s" % self.type or ""
            self.outfile = NamedTemporaryFile(mode='r+', suffix=ext)
            options["outfile"] = os.path.dirname(self.outfile.name)

        # Quote infile and outfile for spaces etc.
        if "infile" in options:
            options["infile"] = shell_quote(options["infile"])
        if "outfile" in options:
            options["outfile"] = shell_quote(options["outfile"])

        try:
            command = self.command.format(**options)
            proc = subprocess.Popen(
                command, shell=True, cwd=self.cwd, stdout=self.stdout,
                stdin=self.stdin, stderr=self.stderr)
            if self.infile is None:
                # if infile is None then send content to process' stdin
                filtered, err = proc.communicate(
                    self.content.encode(encoding))
            else:
                filtered, err = proc.communicate()
            filtered, err = filtered.decode(encoding), err.decode(encoding)
        except (IOError, OSError) as e:
            raise FilterError('Unable to apply %s (%r): %s' %
                              (self.__class__.__name__, self.command, e))
        else:
            if proc.wait() != 0:
                # command failed, raise FilterError exception
                if not err:
                    err = ('Unable to apply %s (%s)' %
                           (self.__class__.__name__, self.command))
                    if filtered:
                        err += '\n%s' % filtered
                raise FilterError(err)

            if self.verbose:
                self.logger.debug(err)

            outfile_path = '{}/{}js'.format(options.get('outfile'), basename)
            if outfile_path:
                with io.open(outfile_path, 'r', encoding=encoding) as file:
                    filtered = file.read()
            filtered = self.wrap_code(filtered, relative_path)
        finally:
            if self.infile is not None:
                self.infile.close()
            if self.outfile is not None:
                self.outfile.close()
        return smart_text(filtered)

    def wrap_code(self, filtered, relative_path):
        wrapper = """
            (function(){{
            window.templates = window.templates || {{}};
            {};
            window.templates["{}"] = template;
            }}());
        """
        return wrapper.format(filtered, relative_path)
