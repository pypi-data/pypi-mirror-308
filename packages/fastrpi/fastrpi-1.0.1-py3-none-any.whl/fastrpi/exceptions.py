import inspect
import linecache


class FastrPIError(Exception):
    """
    This is the base class for all FastrPI related exceptions. Catching this
    class of exceptions should ensure a proper execution of FastrPI.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for all exceptions. Saves the caller object fullid (if
        found) and the file, function and line number where the object was
        created.
        """
        super(FastrPIError, self).__init__(*args, **kwargs)

        # Save first argument as message
        if args and isinstance(args[0], str):
            self.message = args[0]
        else:
            self.message = ''

        # Search the stack for a caller outside this file (to allow subclass
        # constructors not to be assumed to be the caller)
        frame = {}
        for frame_info in inspect.stack():
            info = inspect.getframeinfo(frame_info[0])

            if info.filename != __file__:
                frame = frame_info[0]
                break

        # Extract the caller info
        call_object = frame.f_locals.get('self', None)
        if call_object is not None and hasattr(call_object, 'fullid'):
            self.fastr_object = call_object.fullid
        else:
            self.fastr_object = None

        self.filename = info.filename
        self.function = info.function
        self.linenumber = info.lineno

        # Add a formatted stack trace to the error itself, useful when re-raising the error
        stack = []
        for frame, filename, lino, name, code_contex, index in inspect.stack()[1:]:
            source_line = linecache.getline(filename, lino).strip()
            stack.append('File {f}, line {l} in {n}\n  {s}'.format(f=filename, l=lino, n=name, s=source_line))
        self.stack_trace = '\n'.join(reversed(stack))

    def __repr__(self):
        """
        String representation of the error

        :return: error representation
        :rtype: str
        """
        if self.filename and self.linenumber:
            error_string = '<{} (from {}:{}) {}>'.format(type(self).__name__,
                                                         self.filename,
                                                         self.linenumber,
                                                         self.message)
        else:
            error_string = '<{}: {}>'.format(type(self).__name__, self.message)

        if self.fastr_object is not None:
            return '[{}] {}'.format(self.fastr_object, error_string)
        else:
            return error_string

    def __str__(self):
        """
        String value of the error

        :return: error string
        :rtype: str
        """
        if self.filename and self.linenumber:
            error_string = '{} from {} line {}: {}'.format(type(self).__name__,
                                                           self.filename,
                                                           self.linenumber,
                                                           self.message)
        else:
            error_string = '{}: {}'.format(type(self).__name__, self.message)

        if self.fastr_object is not None:
            return '[{}] {}'.format(self.fastr_object, error_string)
        else:
            return error_string

    def excerpt(self):
        """
        Return an excerpt of the Error as a tuple.
        """
        return type(self).__name__, self.message, self.filename, self.linenumber, self.stack_trace


class FastrPIPublishError(FastrPIError):
    pass


class FastrPIPublishTestError(FastrPIPublishError):
    pass


class FastrPIInstallError(FastrPIError):
    pass


class FastrPINotInstalled(FastrPIInstallError):
    pass


class FastrPIAlreadyInstalled(FastrPIInstallError):
    pass


class FastrPIGitError(FastrPIError):
    pass


class FastrPIDockerError(FastrPIError):
    pass


class FastrPIInputError(FastrPIError):
    pass


class FastrPIManifestError(FastrPIError):
    pass


class FastrPIRunError(FastrPIError):
    pass

class FastrPICreateError(FastrPIError):
    pass
