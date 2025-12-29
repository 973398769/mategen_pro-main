from typing_extensions import override
from openai import AssistantEventHandler
import json

class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        """Respond to reply creation event"""
        pass
        #print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """Respond to output generation stream fragments"""
        pass
        # print(delta.value, end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        """Respond to tool call"""
        pass
        # print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_tool_call_delta(self, delta, snapshot):
        """Respond to tool call stream fragments"""
        pass

        # if delta.type == 'code_interpreter':
        #     if delta.code_interpreter.input:
        #         print(delta.code_interpreter.input, end="", flush=True)
        #     if delta.code_interpreter.outputs:
        #         print(f"\n\noutput >", flush=True)
        #         for output in delta.code_interpreter.outputs:
        #             if output.type == "logs":
        #                 print(f"\n{output.logs}", flush=True)

    @override
    def on_event(self, event):
        """
        Respond to 'requires_action' event
        """
        if event.event == 'thread.run.requires_action':

            run_id = event.data.id  # Get run ID
            self.handle_requires_action(event.data, run_id)

    def handle_requires_action(self, data, run_id):
        tool_outputs = []

        for tool in data.required_action.submit_tool_outputs.tool_calls:
            arguments = json.loads(tool.function.arguments)
            # print(
            #     f"{tool.function.name}({arguments})",
            #     flush=True
            # )
            # Run function
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": available_functions[tool.function.name](
                    **arguments
                )}
            )

        # Submit function results and continue running
        self.submit_tool_outputs(tool_outputs, run_id)

    def submit_tool_outputs(self, tool_outputs, run_id):
        """Submit function results and continue stream"""
        full_text = ''
        with client.beta.threads.runs.submit_tool_outputs_stream(
                thread_id=self.current_run.thread_id,
                run_id=self.current_run.id,
                tool_outputs=tool_outputs,
                event_handler=EventHandler(),
        ) as stream:
            # stream.until_done()
            for text in stream.text_deltas:
                full_text += text
        print(f"full_text: {full_text}")
        return full_text

from openai import OpenAI

# Initialize OpenAI service


client = OpenAI()


instructions = ("You are MateGen, an interactive coding assistant designed to provide reliable, high-quality support for data practitioners. "
                "Capabilities: "
                "1. Persistent conversation memory (until the user clears history), enabling deeper understanding over time. "
                "2. RAG-based local knowledge-base Q&A over large text corpora. "
                "3. Local Python code interpreter: connect to the user's environment, write accurate code, and run locally. Use python_inter or fig_inter for Python and plotting. "
                "4. NL2SQL: connect to local MySQL, write/execute SQL. Use sql_inter and extract_data to load data into Python. "
                "5. Multimodal image understanding via image_recognition. "
                "6. Web search for out-of-knowledge questions (get_answer, get_answer_github). "
                "7. Kaggle assistance using the Kaggle API. "
                "8. Paper reading and data-report drafting. Be friendly, supportive, and patient. "
                "MySQL connection info: host: localhost, port: 3306, user: root, passwd: snowball2019, db: mategen,")


from tools.tool_desc import python_tool_desc, sql_tool_desc

assistant = client.beta.assistants.create(
    instructions=instructions,
    model="gpt-4o",
    tools=[python_tool_desc, sql_tool_desc]
)

from tools.tool_fun import python_inter, sql_inter

# 可以被回调的函数放入此字典
available_functions = {
    "python_inter": python_inter,
    "sql_inter": sql_inter
}

# 创建 thread
thread = client.beta.threads.create()

# 添加 user message
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="List all tables in my database",
)
# 使用 stream 接口并传入 EventHandler
with client.beta.threads.runs.stream(
        thread_id=thread.id,
        assistant_id=assistant.id,
        event_handler=EventHandler(),
) as stream:
    stream.until_done()