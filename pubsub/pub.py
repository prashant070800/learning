from google.cloud import pubsub_v1
from google.oauth2 import service_account
# cd 

def publish_message(project_id, topic_id, message, credentials_file):
    # Load credentials from the service account file
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    
    # Create a Publisher client with explicit credentials
    publisher = pubsub_v1.PublisherClient(credentials=credentials)
    topic_path = publisher.topic_path(project_id, topic_id)

    # Publish a message
    future = publisher.publish(topic_path, message.encode("utf-8"))
    print(f"Published message ID: {future.result()}")

if __name__ == "__main__":
    project_id = "pub-sub-433616"
    topic_id = "learning"
    message = "Hello, World!"
    credentials_file = "pub-sub-key.json"

    publish_message(project_id, topic_id, message,credentials_file)
