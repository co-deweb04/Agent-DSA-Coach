from conversation import (
    create_conversation,
    save_message,
    get_messages,
    get_conversations
)


conversation_id = create_conversation("Two Sum Discussion")

print("Conversation ID:", conversation_id)


save_message(
    conversation_id,
    "user",
    "Explain Two Sum"
)

save_message(
    conversation_id,
    "assistant",
    "Two Sum is a problem where we find two numbers whose sum equals the target."
)


messages = get_messages(conversation_id)

print("\nMessages:")

for role, content in messages:
    print(role, ":", content)


print("\nAll Conversations:")

print(get_conversations())