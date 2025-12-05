# <center>Large Model AI Agent Development Practice

## <center>Ch.1 Large Model Application Development and Agent Technology Trends

&emsp;&emsp;Since early 2023, large models have attracted tremendous attention both domestically and internationally. In fact, as early as late 2022, there were already very intense discussions about this technology abroad, while the popularization and recognition of large models in China largely benefited from the advent of `ChatGPT`. This phenomenal conversational application directly changed people's perceptions of intelligent applications. Before this, we had become accustomed to the mechanical responses of `intelligent customer service` and the frequent errors of `intelligent applications`. So when an application system appeared that could understand emotions using `natural language` (i.e., human communication language), solve problems, and provide immediate responses, it was hard for people to believe that behind it was not a real human being, but a machine model designed by humans.

&emsp;&emsp;The conversation in the image below comes from the conversational application `ChatGPT` based on the `GPT-4.0` model 👇

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240828150834951.png" width=80%></div>

&emsp;&emsp;As shown in the image above, we can use the most natural conversational approach to have the large model help us handle various tasks, solve problems, learn new knowledge, and even provide comfort when needed. It behaves like an omniscient and omnipotent friend. Whenever you need it to play a different role, simply **create a new conversation window**, and it can transform into a brand-new companion. Before its emergence, whether machine learning models or deep learning models in the field of artificial intelligence, they all required training on specific data before they could perform specific tasks, such as classification tasks in machine learning or entity recognition in deep learning. Large models, with their near-human interactive characteristics, have transcended these boundaries, using **independent entities** to directly solve various types of problems, and performing quite well, directly pushing the popularity of artificial intelligence to new heights.

&emsp;&emsp;It is precisely this technological leap that makes industry insiders call 2023 the **Year One of Large Models**, because it marks a new stage for artificial intelligence, and the era of large models has only just begun. So as technical professionals, we are definitely not just "spectators" - while watching the excitement, more energy is devoted to actively following the development of large models, deeply understanding and mastering the technological evolution behind them, thereby continuously updating our technical vision. **Of course, what we need to study is not the surface application `ChatGPT`, but the powerful foundation model behind it - `GPT`.**

# 1. Rapid Iteration of Large Model Applications

&emsp;&emsp;What's quite interesting is that if there are friends from **non-technical positions** who have been using `ChatGPT`-like applications since 2023, they would most likely have such thoughts: the technological development of large models over the past year and a half has not brought significant product changes - it's just that the interface has become more aesthetically pleasing and some functions have been added, such as now supporting image uploads, file uploads, and plugin development. But looking at the essence through the surface application, you'll find that the iteration speed of large model technology is far faster than other fields. Its rapid development has two core directions:

1. **The capabilities of large models themselves are constantly strengthening**
2. **The conversational effectiveness of large models is significantly improving**

&emsp;&emsp;The technology stack iterations behind these two directions can be summarized as shown in the diagram below 👇:

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/02.png" width=80%></div>

- **The capabilities of large models themselves are constantly strengthening**

&emsp;&emsp;**Large models have two key concepts: native capabilities and emergent capabilities.**

&emsp;&emsp;So-called **native capabilities** refer to the ability of large models to solve problems in specific domains through continuous data ingestion during training, based on a specific neural network architecture. This capability is like knowledge imprinted in the large model's "brain" and is the foundation for its ability to independently answer questions. Just as we can solve advanced mathematics problems after three years of university study, this capability is acquired through learning, and we call it native capability. The improvement of this capability in large models lies in: as the amount of accessible data increases, developers can construct higher-quality learning data based on previous performance, combined with continuous iterative optimization of learning methods (technically called pre-training or fine-tuning), allowing the native capabilities of large models to continuously evolve. **The intuitive manifestation of this progress is the improvement of the model's comprehension ability and answer quality.**

&emsp;&emsp;Secondly, we also focus on the **emergent capabilities** of large models. This capability refers to the fact that although large models may not have directly learned certain information, after providing relevant information during conversation, they can reason by analogy and deduce solutions. This is similar to when we prepare for college entrance exams by doing "Five Years of College Entrance Exams, Three Years of Simulations" - although the actual exam questions won't be exactly the same as the simulation questions, we can still use the same thinking patterns to solve the test problems. The improvement of this aspect of large models' capabilities is mainly reflected in: we construct various function calls and process examples for complex problems (Agent capabilities) during the pre-training or fine-tuning stage to help it learn and strengthen this ability. In this way, large models can play a more important role in the second direction of their application - i.e., in solving practical problems.

> Regarding the principles and applications of pre-training and fine-tuning, we will introduce them in detail in the fine-tuning column of this video series.

- **The conversational effectiveness of large models is significantly improving**

&emsp;&emsp;The capabilities of large models are undoubtedly strong - they can answer and solve many different types of tasks during conversations, but there are two main problems: **untimely knowledge base updates and the large model hallucination problem**.

&emsp;&emsp;First, regarding the knowledge base update issue, as we just mentioned above, large models acquire and learn knowledge during the pre-training or fine-tuning stage. This means that if some latest information is not included in the training data, the large model cannot provide relevant answers. For example, if you ask it "What's the weather like today?" Due to the lack of real-time updated data, the large model cannot give the correct current weather conditions.

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240828170408714.png" width=80%></div>

&emsp;&emsp;What's quite interesting is: the native capabilities of large models are continuously improving, their conversational effectiveness has improved, and their answer quality is higher, but our demands have also become more and more complex. Pure conversational applications can no longer meet the needs. This prompted us to enter the first stage of large model applications - **Prompt Engineering**.

- **Stage 1: Prompt Engineering**

&emsp;&emsp;Although large language models are very powerful, using them effectively is not easy. While developers were eager to explore how to quickly iterate and update the internal knowledge of large models through fine-tuning like traditional algorithmic models, a highly inspiring paper 👉 [GPT-3 Language Models are Few-Shot Learners](https://arxiv.org/pdf/2005.14165) proposed the concept of `In-Context Learning`. This method can significantly improve the output quality of large models by providing a small number of labeled "input-output pair" examples to the model, without requiring large-scale fine-tuning. This discovery opened up a new way of using large models 👇

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240828172452210.png" width=80%></div>

&emsp;&emsp;After posing a question, large models can return responses in natural language, which is a major advantage of generative artificial intelligence. Some tasks can indeed guide large models to generate correct replies during conversations through this prompt engineering approach, but the biggest problem with this process is that it requires human intervention, just like the Beijing weather information involved in the example above:

```json
{
  "location": {
    "city": "Beijing",
    "country": "CN",
    "timezone": "Asia/Shanghai",
    "coordinates": {
      "latitude": 39.9042,
      "longitude": 116.4074
    }
  },
  "current": {
    "temperature": {
      "value": 34,
      "unit": "C"
    },
    "humidity": 55,
    "pressure": {
      "value": 1012,
      "unit": "hPa"
    }
  },
  "sunrise": "2024-08-28T05:45:00+08:00",
  "sunset": "2024-08-28T19:18:00+08:00"
}
```

&emsp;&emsp;For developers trying to connect large model responses with other applications, this is a nightmare. Developers typically use regular expressions (Regex) or prompt engineering to convert the output into the desired format before passing it to another application. That is to say, if human intervention is not required in this process and we still want it to automatically obtain this information, how do we do it?

&emsp;&emsp;Friends who have done development should be very familiar with this type of JSON data. We can call an API from a weather platform, such as 👉 [OpenWeather](https://openweathermap.org/), input a city keyword, and get the current weather information data for that city, which is in JSON format as shown above. So how can we make large models automatically parse such information? This leads us to explore the second stage of large model applications - **Function Calling**.

- **Stage 2: Function Calling**

&emsp;&emsp;In July 2023, OpenAI introduced function calling capabilities for its GPT models. As large models have developed to the present, all popular large models have acquired function calling capabilities in different forms. Through function calling, we can provide a user-defined JSON string that contains **the response structure we hope to get from the large model** and **the question we want to ask the large model**. As shown in the diagram below, we conceptually demonstrate how it works:

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/03.png" width=60%></div>

&emsp;&emsp;The **callable functions** referred to here are commonly called **tools**. At this stage, what we need to do is describe what the tool is used for, and then let the large model intelligently choose to output a JSON object containing parameters for calling these functions. In simple terms, it allows:
- Autonomous decision-making: Large models can intelligently select tools to answer questions.
- Reliable parsing: Responses are in JSON format, rather than the more typical conversation-like responses.

&emsp;&emsp;At first glance, it may seem insignificant, but this is why large models can connect to external systems, such as through APIs with structured input, local databases, Python code functions you write yourself, etc. With this capability, large models have opened up infinite possibilities in applications. For example:

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240828180451679.png" width=80%></div>

&emsp;&emsp;When large models are given function calling capabilities, they check which tools can be called before answering each question and evaluate whether the user's question requires calling these tools. If needed, it will call the corresponding tool and construct the answer based on the results returned by the tool. This entire process is based on the large model's autonomous judgment. So improving at this stage not only greatly expands the application scope of large models but also to some extent solves the problems of untimely knowledge base updates, inability to obtain real-time information, and the advantages it brings.

> Regarding the function calling (Function Calling) capability of large models, we will introduce its theory in detail and conduct case practice in the upcoming courses.

&emsp;&emsp;However, as function calling technology matured, we still discovered another very significant problem: large model hallucination 👇

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240828181631010.png" width=80%></div>

&emsp;&emsp;Large models still commonly have a problem even now: when faced with questions they don't understand, they sometimes produce inaccurate or even absurd answers. This is the so-called **large model hallucination problem**. Taking the example in the image above, when a large model is asked questions about company policies, without any technical intervention, the ideal answer should be "I don't know" or "Please provide the specific policies of the company you're joining," etc. But what we see is the large model incorrectly responding from an HR perspective, which can confuse and mislead users.

&emsp;&emsp;In `Stage 1: Prompt Engineering`, we mentioned that large models can answer specific questions based on background information provided using the `in-context learning` prompt idea, which directly triggered the first wave of large model application implementation, mainly concentrated in the **local knowledge base Q&A field**. Because whether individuals or enterprises, everyone hopes that large models can accurately and efficiently answer questions based on their private data - such as personal learning materials or company regulations - acting as intelligent customer service or intelligent assistants. However, a significant challenge is that the data volume may be extremely large, from a single file to thousands of GBs of file systems, while large models have input length limits in conversation processing and cannot directly process all data as background information.

&emsp;&emsp;Therefore, facing the challenges of local knowledge base Q&A and considering the hallucination problem and length limitation problem of large models, the solution that emerged is: RAG (Retrieval-Augmented Generation), thus entering the third stage of large model applications.

- **Stage 3. Retrieval-Augmented Generation**

&emsp;&emsp;Through people's continuous exploration of the large model field, numerous experimental papers can prove that when providing certain contextual information to large models, their output becomes more stable. So, first delivering information from the knowledge base or possessed information to the large model, and then having the large model serve users, is a conclusion and method that everyone generally reaches consensus on. Traditional dialogue systems and search engines rely heavily on retrieval technology. If this retrieval process is integrated into the construction of large model applications, it can not only fully utilize the capabilities of large models in content generation but also significantly constrain the output scope and results of large models through the introduced contextual information, while also achieving the purpose of integrating private data into large models, achieving a win-win effect.

&emsp;&emsp;So we see that RAG implementation includes two stages: the retrieval stage and the generation stage. In the retrieval stage, the most relevant knowledge is found from the knowledge base to provide material for subsequent answer generation. In the generation stage, RAG takes the retrieved knowledge content as input and inputs it into the language model together with the question for generation. In this way, the generated answer not only considers the semantic information of the question but also considers the content of relevant private data. For example, the RAG process we implemented in our "RAG Enterprise-level Project Practice Course" 👇

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/1234.png" width=80%></div>

&emsp;&emsp;The two key problems that RAG technology solves are:
1. If the answer to a question posed by a user appears in an article, it's easy to find an article related to the user's input in the knowledge base, but putting the entire retrieved article directly into the `Prompt` is not the optimal choice because it will definitely contain a lot of irrelevant information, and the more invalid information there is, the greater the impact on the large model's subsequent reasoning.

2. Any large model has a maximum input Token limit. A process may involve multiple retrievals, and each retrieval generates corresponding context, which cannot accommodate so much information.

&emsp;&emsp;But in fact, as shown in the flowchart above, large models actually occupy a very small proportion in the entire RAG architecture. We mainly rely on large models' ability to reason combined with background information. In the multiple optimization stages of RAG, the role of retrieval strategies is more important. Additionally, RAG's actual application scenarios are relatively limited. No matter what form of Q&A system, none has reached the level of Artificial General Intelligence (AGI) we expect. Therefore, **at the current stage, we have entered the full explosion of `AI Agent`, a technology that directly represents our development towards more complex and comprehensive technological directions we expect.**

&emsp;&emsp;So what is Artificial General Intelligence? Why can AI Agent achieve general artificial intelligence?

# 2. AI Agent Application Explosion

&emsp;&emsp;In the field of artificial intelligence technology, **the only type of artificial intelligence successfully developed so far is Artificial Narrow Intelligence (ANI), also known as weak artificial intelligence**. It refers to artificial intelligence systems that perform specific tasks or a set of closely related tasks. ANI does not replicate human intelligence but simulates human behavior within a limited range of parameters and contexts. Examples include image generation and recognition, natural language processing, computer vision, etc. AI systems in autonomous vehicles, recommendation engines, Siri, Google Assistant, and Alexa are all forms of narrow artificial intelligence. Significant breakthroughs in narrow artificial intelligence are largely attributed to advances in machine learning and deep learning, powered by natural language processing (NLP), enabling them to understand and process human language. For example, AI systems are now used in medicine to diagnose cancer and other diseases with high precision.

&emsp;&emsp;The Artificial General Intelligence (AGI) we now hope to achieve refers to **artificial intelligence with capabilities equivalent to or exceeding human capabilities. It encompasses the ability to learn, understand, and apply knowledge across different domains. AGI is also known as strong artificial intelligence.**

&emsp;&emsp;So you can feel that there is a fundamental difference between the artificial intelligence we have achieved at the current stage and Artificial General Intelligence. Although applications like `ChatGPT` have sparked a new wave of enthusiasm, they are essentially just "predicting" - training with large amounts of data to achieve the purpose of generating accurate responses, but lacking the concept of goals, identity, or autonomous decision-making. So they are just complex text generators, without a sense of purpose or direction. We haven't fully achieved AGI yet because every existing AI model only mimics some aspect of human intelligence. For example, large language models are very good at understanding and writing text, and their capabilities often surpass human performance in these areas. However, when it comes to simple arithmetic tasks, LLMs often have problems.

&emsp;&emsp;So **to let large models solve more complex problems by themselves, the solution proposed at the current stage is: AI Agent.**

&emsp;&emsp;As early as 2016, reinforcement learning agents were hyped up, with people trying to create different types of reinforcement learning agents to play games to judge the intelligence of such agents. There was no concept of AI agents at that time. OpenAI conducted a series of research, including exploring the application of reinforcement learning (RL) in different fields, such as games and web navigation. Among them, a project called "World of Bits" was training AI agents to perform tasks in complex web environments, such as ordering goods or services. This project was one of the explorations of the potential application of reinforcement learning technology in real-world tasks. Paper: 👉 [World of Bits: An Open-Domain Platform for Web-Based Agents](https://proceedings.mlr.press/v70/shi17a/shi17a.pdf)

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240829100032426.png" width=80%></div>

&emsp;&emsp;As shown in the image above, multiple web interfaces shown in this paper are each associated with a specific query question, used to demonstrate different types of online tasks or services. Specifically including:

1. **Flight booking**: Booking flights from San Francisco to New York.
2. **Restaurant search**: Finding the best Korean restaurants in San Francisco.
3. **Loan calculator**: Calculating monthly payments for a $2000 loan over two years.
4. **Product price query**: Querying the price of iPhone 7 Plus in Indiana.
5. **Word search**: Finding a 9-letter word using the letters "sycopthat".
6. **Recipe search**: Finding recipes without chicken but including relevant operations or execution.

&emsp;&emsp;These examples show how AI can help handle various online activities, from searching for information to processing specific requests like shopping or queries. The purpose of this technology is to simplify users' daily tasks through automation and improve efficiency, which can potentially be achieved through intelligent agents or specific applications. Such systems are typically integrated into websites or applications, allowing users to interact through natural language queries, with the system returning relevant answers or executing relevant operations. It seems simple, but this isn't as simple as we think now. It's like autonomous vehicles - easy to imagine, easy to create proof of concept, but difficult to make truly usable.

&emsp;&emsp;**OpenAI's continuous research kept failing to get good results, and we believe the main reason is the absence of what only appeared now: large models.**

&emsp;&emsp;As early as mid-2023, OpenAI, as a technical leader in the entire large model industry, launched the GPT Plugins store very early, leveraging the power of large models to restart related research and hoping to create an ecosystem similar to the APP Store, allowing everyone to create their own intelligent applications with extremely low barriers, whether for personal use or serving others. However, until now, GPT Plugins has not achieved its original intention, and usage has not reached expectations. The main reason is that if the reinforcement learning solution is transplanted to large models, this approach doesn't seem to produce immediate effects. This directly led to GPT Plugins being able to develop intelligent applications, but these applications are still far from meeting our high requirements for complexity and functionality, nor have they reached our expected heights for AI applications. At the same time, I believe that the insufficient capabilities of large models themselves in 2023 are also the fundamental reason for this situation.

&emsp;&emsp;Humans have the extraordinary ability to continuously absorb information, make decisions, take actions, observe changes, and then make the next decision. Our entire life is an endless chain of observation, thought, and action. By breaking down complex problems into smaller, manageable parts and continuously drawing on knowledge from previous generations, we humans have made great strides. **The ultimate form of Artificial General Intelligence is: we can transfer this concept to large models, enabling them to continuously make new decisions, thereby gradually approaching solutions to more complex problems.**

&emsp;&emsp;Thus, the basic concept of AI Agent (Artificial Intelligence Agent) has emerged: **a software program or system that perceives the environment, processes information, and takes actions to achieve specific goals.** At the current stage, we regard a single large model as the core of AI Agent, not the whole. It should be a super good large language model that can interpret problems, observe the environment, and make decisions accordingly. If we add some models that convert speech to text and interpret image content in the AI Agent construction process, we can build everything needed for our own `Jarvis`. (Tony Stark's personal virtual assistant in the Avengers movies)

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/04.png" width=60%></div>

&emsp;&emsp;As shown in the diagram above, it describes the workflow of how an Artificial General Intelligence (AGI) processes user inquiries. The user asks AGI a question through voice, AGI first parses and understands this question, then searches relevant stored documents or online information. Based on the searched information, AGI generates an appropriate answer, such as explaining that it cannot find specific information related to the user's question. Finally, AGI converts the generated text answer into speech output to provide a response to the user. The entire process shows how AGI uses existing resources to understand and respond to complex human inquiries. From this process, we can clearly understand **why AGI implementation needs to focus on AI Agents rather than a single large model.**

&emsp;&emsp;It's easy to explain: through prompt engineering, large models can generate more human-like responses. But when we apply the concept of agents, we use large models not just to answer questions, but as a brain to process the observations it sees and decide what to do next. This is how humans process problems: if there's a task that needs to be solved, we often look for methods and tools that can help us solve that task as easily as possible. If we don't equip large models with enough tools, even if they know what to do, without the ability to call tools, everything becomes empty talk.

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240828103858977.png" width=80%></div>

&emsp;&emsp;Fundamentally, unlike traditional automation systems that strictly follow set scripts or task sequences, AI agents have the ability to perceive, interpret, learn, and adapt. Think of them as digital assistants that not only perform tasks but also continuously evaluate their surroundings, learn from different interactions, and make decisions to achieve specific goals. They can take many forms, from simple software that performs a single task to complex systems that manage complex processes. AI agents excel in unpredictable environments where their adaptability and learning capabilities can be fully utilized. From browsing the internet, interacting with applications, processing large amounts of data to participating in transactions, all these tasks can be delegated to AI agents.

# 3. Theory Behind AI Agent

&emsp;&emsp;The human advantage is the ability to absorb relatively large amounts of information, filter out unimportant details, and make decisions based on key information. For example, before dealing with something, we usually first break down the big problem into small assumptions, then try to support or refute these assumptions through gradual observation. **From this realistic perspective, a paper that inspired the early paradigm of AI Agent 👉 [REACT: SYNERGIZING REASONING AND ACTING IN LANGUAGE MODELS](https://arxiv.org/pdf/2210.03629) uses "chain-of-thought prompting" to simulate this concept, breaking down multi-step problems into intermediate steps:**

- Initiate an action, letting the large model observe the feedback from the selected environment
- Gather all information in the process and use it to decide what appropriate action to take next
- Iteratively execute this to solve larger, more complex tasks, using a method called "reasoning trace," which involves tracking the steps or stages the entire process goes through to reach a conclusion or solution

&emsp;&emsp;As shown in the diagram below, the entire process is a dynamic cycle. The agent continuously learns from the environment, influences the environment through its actions, and then continues to adjust its actions and strategies based on environmental feedback. This pattern is particularly suitable for application scenarios that require understanding and generating natural language, such as chatbots, automatic translation systems, or other forms of automated customer support.

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/05.png" width=60%></div>

&emsp;&emsp;A more sensory understanding is shown in the diagram below:

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/06.png" width=80%></div>

&emsp;&emsp;As shown in the diagram above, it displays the basic architecture of an AI agent, including its interaction with the environment, perceptual input, brain processing, and decision-making process. Specifically:

1. **Environment**: The AI agent receives information from its surrounding environment. The environment can be a website, database, or any other type of system.
2. **Perception** (Input): The AI agent perceives the environment through various means, such as vision (images), hearing (sound), text (text information), and other sensor inputs (such as location, temperature, etc.). These inputs help the agent understand the current environmental state.
3. **Brain**:
   - **Storage**:
     - **Memory**: Stores previous experiences and data, similar to human memory.
     - **Knowledge**: Includes facts, information, and programs the agent uses for decision-making.
   - **Decision Making**:
     - **Summary**, **Recall**, **Learn**, **Retrieve**: These functions help AI review and utilize stored knowledge when needed.
     - **Planning/Reasoning**: Based on current input and stored knowledge, formulate action plans.
4. **Action**: The agent generates responses or actions based on its perception and decision-making process. This can be physical actions, sending API requests, generating text, or other forms of output.

&emsp;&emsp;So from this process, we can abstract the most classic basic framework of AI Agent, which is also currently the basic framework of any Agent framework, as shown in the diagram below:

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/image-20240829111123754.png" width=80%></div>

> Image source: https://lilianweng.github.io/posts/2023-06-23-agent/, strongly recommend everyone to read it thoroughly.

&emsp;&emsp;This **intelligent agent architecture refers to the structured design of autonomous agents**, autonomous agents are systems or entities that can independently perceive the environment, make decisions, and take actions to achieve specific goals. This architecture describes how the various components of an agent interact to facilitate intelligent behavior. The architecture includes four key components:

- Planning: This component places the agent in a dynamic environment, enabling it to formulate strategies and plan future actions based on its goals and collected information.
- Memory: This component enables the agent to recall past behaviors, experiences, and outcomes, which is crucial for learning and adaptation.
- Action: This component translates the agent's decisions into concrete actions, executing planned tasks to achieve desired outcomes.
- Tools: Having an agent with only an LLM is like using a computer without any additional equipment. Tools enable agents to use the internet, gain specialized knowledge, or work with several different AI models that excel at specific things, making the agent more useful.

&emsp;&emsp;AI agents are characterized by their proactivity and decision-making abilities. Unlike passive tools, they actively participate in the environment, make choices, and take actions to achieve their specified goals. In enterprise environments, AI agents improve efficiency by automating routine tasks and analyzing complex data, thereby enabling employees to focus on strategic and creative work. These agents complement rather than replace human efforts, facilitating increased workforce productivity and efficiency.

&emsp;&emsp;Let's imagine a scenario with Li Hua, a sales manager in the Chinese market, and his AI assistant.

&emsp;&emsp;Li Hua's workday begins with checking emails. He receives an email from Zhang Wei, a potential client interested in the efficient solutions his company offers. Li Hua's AI assistant is directly connected to his email system and monitors these interactions in real-time. Based on Li Hua's past response habits and the company's information base, the AI assistant drafts a detailed reply. The email not only summarizes the company's efficient solutions and their advantages but also provides customized recommendations based on Zhang Wei's needs.

&emsp;&emsp;Li Hua reviews the draft email, adds some personalized statements to appear more friendly and professional, and then sends it to Zhang Wei. Subsequently, the AI suggests follow-up steps including scheduling a phone conference with Zhang Wei, sending a detailed product introduction handbook, or if there's no response within a week, reminding Li Hua to follow up. Li Hua agrees with these suggestions, and the AI assistant immediately organizes his schedule, sends the product handbook via email, and sets follow-up reminders in his electronic calendar. By having AI handle these routine but critical tasks, Li Hua can devote more energy to other important business development activities.

&emsp;&emsp;Key capabilities demonstrated by AI Agent in this process:
- AI Agent utilizes the inherent language understanding capabilities of large models to interpret instructions, context, and goals. This enables them to operate autonomously or semi-autonomously based on human prompts.
- AI Agent can use various tools (reading emails, calculators, search engines, etc.) to gather information and take actions to complete assigned tasks. Their capabilities go beyond mere language processing.
- AI Agent can demonstrate complex reasoning techniques, establishing logical connections to draw conclusions and solve problems, not just simple text understanding.
- AI Agent can generate customized text for specific purposes, such as emails, reports, and marketing materials, by integrating context and goals into its language generation capabilities.
- AI Agent agents can operate fully autonomously or semi-autonomously, requiring different levels of interaction with users.

&emsp;&emsp;The benefits of AI agents go beyond efficiency. They create collaborative environments, reduce the risk of human error, and free up valuable time for creative and strategic thinking. Essentially, AI agents are not just tools. They are partners that complement human capabilities and drive innovation.

# 4. Agent Behind the Agent

&emsp;&emsp;What needs to be clarified next is that AI Agents can continuously execute the correct tools, constantly observe results, and then decide what kind of tool is needed next. This iterative execution of functions is performed by the `AgentExecutor`. `AgentExecutor` refers to when an agent runs, the entire process is repeated over and over until predefined termination criteria are met. As enterprises recognize the upcoming AI agent revolution, solution providers are emerging, offering tools and frameworks that make building these AI agents easy. From no-code, low-code to complete Python libraries and more. The list of frameworks and tools is simply dazzling. But the most fundamental difference is nothing more than extensions based on the classic Agent framework and different `AgentExecutor` construction concepts and processes.

&emsp;&emsp;Each `AgentExecutor` has its own method and approach to executing tasks and making decisions. The choice of `AgentExecutor` mainly depends on the specific requirements of the task at hand, the complexity of the decision-making process, and the level of autonomy or intelligence desired for the agent to exhibit. Different `AgentExecutors` also form multiple different products and tools. Here we provide a navigation website that provides a good summary and organization of AI Agent tools: https://e2b.dev/ai-agents/open-source 👇

<div align=center><img src="https://muyu001.oss-cn-beijing.aliyuncs.com/img/landscape-latest.png" width=80%></div>

&emsp;&emsp;Among the above frameworks, our course will select popular and mainstream ones like AutoGPT, CrewAI, LangGraph, etc., and introduce their principles and application skills in detail in subsequent courses. At the same time, everyone can also try selecting the most suitable tools for their current tasks and work needs based on the project list on the navigation website.

&emsp;&emsp;AI agents represent a transformative force in the technology field. Their capabilities, from simple automation to the ingenuity demonstrated by systems like Devin, are rapidly expanding. We are witnessing their success in everyday tasks such as customer service and virtual assistance, and this is just the beginning. Supported by increasingly complex large models, a new generation of AI agents ushers in an era of unprecedented efficiency and innovation. As enterprises adopt AI agents at scale, the demand for skilled personnel (people who can design, deploy, and manage these systems) will surge. Beyond potential job losses in certain industries, AI will also create exciting new careers. To thrive in this constantly changing environment, we must have adaptability and continuous learning capabilities.

&emsp;&emsp;Understanding different types of AI agents, their core workflow steps, and the powerful frameworks supporting their creation is key. Our course will also proceed step by step along this solid technical route.
