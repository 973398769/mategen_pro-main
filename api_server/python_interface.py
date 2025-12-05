
import sys
from io import StringIO
import traceback
import io
import matplotlib
import base64
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import warnings

def execute_python_code(code: str, output_directory="images") -> dict:
    redirected_output = io.StringIO()
    images = []

    # Prepare a dictionary to serve as global variables for execution environment
    exec_globals = {
        "__builtins__": __builtins__,
        "__name__": "__main__",
    }

    try:
        # Redirect standard output, capture print() and other outputs
        with redirect_stdout(redirected_output):
            # Suppress UserWarning warnings
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)

                # Redefine plt.show() to make it do nothing
                plt.show = lambda: None

                # Execute code
                exec(code, exec_globals)

        # Get all generated figures
        figs = [plt.figure(num) for num in plt.get_fignums()]
        for fig in figs:
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            # Encode image as base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            images.append(img_base64)
            buf.close()
            plt.close(fig)  # Close figure, release memory

    except Exception as e:
        # Capture and return exception type and message
        error = f"{type(e).__name__}: {e}"
        stdout = redirected_output.getvalue()
        redirected_output.close()
        ans = {'stdout': stdout, 'error': error, 'images': images}
        return ans  # Return dictionary containing error information
    else:
        stdout = redirected_output.getvalue()
        redirected_output.close()
        ans = {'stdout': stdout, 'error': None, 'images': images}
        return ans  # Return normal execution result

if __name__ == '__main__':
    code = "print(123)"
    ans = execute_python_code(code)
    print(ans)
    # with CodeInterpreter(api_key="e2b_6cd364fa5d0889be24a0aecb60ca06aba929dd23") as sandbox:
    #     execution = sandbox.notebook.exec_cell(code)
    #     if execution.error:
    #         err_msg = f"{execution.error.name}:{execution.error.value}"
    #         print(err_msg)
    #
    #     if execution.logs.stdout or execution.logs.stderr:
    #         message = ""
    #         if execution.logs.stdout:
    #             message += "\n".join(execution.logs.stdout) + "\n"
    #
    #         if execution.logs.stderr:
    #             message += "\n".join(execution.logs.stderr) + "\n"
    #
    #         print(message)

    # print(execution)
    # print(execution.logs.stdout[0])
