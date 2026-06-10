import time
import random
import threading
import boto3
from bedrock_agentcore.memory import MemorySessionManager
from bedrock_agentcore.memory.constants import ConversationalMessage, MessageRole

region_name="ap-southeast-1"
control_client = boto3.client('bedrock-agentcore-control', region_name=region_name)

# Retrieve the memory created in Step 1
response = control_client.list_memories()
memory = response['memories'][0]
memory_id = memory['id']
count = 10

session_id="OrderSupportSession1"
session_manager = MemorySessionManager(
    memory_id=memory_id,
    region_name=region_name)


def search_memory(session, actor_id, namespace_path, top_k):
    start = time.time()
    memory_records = session.search_long_term_memories(
        query="can you summarize the support issue",
        namespace_path=namespace_path,
        top_k=top_k
    )
    elapsed = time.time() - start
    print(f"[{actor_id}] memory_records: {len(memory_records)}, elapsed: {elapsed:.3f}s")
    return memory_records

def query():
    print("本轮开始，并发数：", count)
    threads = []  # 用来保存所有线程
    for _ in range(count):
        i = random.randint(0, 100)
        actor_id = "user-" + str(i)
        session = session_manager.create_memory_session(
            actor_id=actor_id,
            session_id=session_id
        )
        t=threading.Thread(
            target=search_memory,
            args=(session, actor_id, "/", 3),
            daemon=True
        )
        t.start()
        threads.append(t)  # 存起来
    # 🔥 等待所有线程执行完毕
    for t in threads:
        t.join()

    # 这里会等所有 query_memory 跑完才执行！
    print("✅ 本轮完成!")
    return

if __name__ == "__main__":
    while True:
        query()
        time.sleep(1)
