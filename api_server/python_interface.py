
import sys
from io import StringIO
import traceback
import io
import matplotlib
import base64
matplotlib.use('Agg')  # 使用非交互式后端
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
import warnings

def execute_python_code(code: str, output_directory="images") -> dict:
    redirected_output = io.StringIO()
    images = []

    # 准备一个字典来作为执行环境的全局变量
    exec_globals = {
        "__builtins__": __builtins__,
        "__name__": "__main__",
    }

    try:
        # 重定向标准输出，捕获 print() 等输出
        with redirect_stdout(redirected_output):
            # 抑制 UserWarning 警告
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=UserWarning)

                # 重定义 plt.show()，使其不执行任何操作
                plt.show = lambda: None

                # 执行代码
                exec(code, exec_globals)

        # 获取所有生成的图形
        figs = [plt.figure(num) for num in plt.get_fignums()]
        for fig in figs:
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            # 将图片编码为 base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            images.append(img_base64)
            buf.close()
            plt.close(fig)  # 关闭图形，释放内存

    except Exception as e:
        # 捕获并返回异常的类型和消息
        error = f"{type(e).__name__}: {e}"
        stdout = redirected_output.getvalue()
        redirected_output.close()
        ans = {'stdout': stdout, 'error': error, 'images': images}
        return ans  # 返回包含错误信息的字典
    else:
        stdout = redirected_output.getvalue()
        redirected_output.close()
        ans = {'stdout': stdout, 'error': None, 'images': images}
        return ans  # 返回正常的执行结果

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
