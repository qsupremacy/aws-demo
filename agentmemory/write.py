import boto3
from bedrock_agentcore.memory import MemorySessionManager
from bedrock_agentcore.memory.constants import ConversationalMessage, MessageRole

region_name="ap-southeast-1"
control_client = boto3.client('bedrock-agentcore-control', region_name=region_name)

# Retrieve the memory created in Step 1
response = control_client.list_memories()
memory = response['memories'][0]
memory_id = memory['id']
session_id="OrderSupportSession1"

for i in range(1, 101):
    actor_id = f"user{i}"
    session_manager = MemorySessionManager(
        memory_id=memory_id,
        region_name=region_name)

    session = session_manager.create_memory_session(
        actor_id=actor_id,
        session_id=session_id
    )

    session.add_turns(
        messages=[
            ConversationalMessage(
                "Hi, how can I help you today?",
                MessageRole.ASSISTANT)],
    )

    session.add_turns(
        messages=[
            ConversationalMessage(
                f"Hi, I am {actor_id}. I just made an order, but it hasn't arrived. The Order number is #35476",
                MessageRole.USER)],
    )

    session.add_turns(
        messages=[
            ConversationalMessage(
                "I'm sorry to hear that. Let me look up your order.",
                MessageRole.ASSISTANT)],
    )

    memory_records = session.search_long_term_memories(
        query="can you summarize the support issue",
        namespace_path="/",
        top_k=3
    )
    print("memory_records:", actor_id, len(memory_records))
    
    #for record in memory_records:
    #    print(f"[{actor_id}] Memory record: {record}")
    #    print("--------------------------------------------------------------------")
