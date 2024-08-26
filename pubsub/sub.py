from google.cloud import pubsub_v1
from google.oauth2 import service_account

def pull_messages(project_id, subscription_id,credentials_file):
    # Create a Subscriber client
    credentials = service_account.Credentials.from_service_account_file(credentials_file)

    subscriber = pubsub_v1.SubscriberClient(credentials=credentials)
    subscription_path = subscriber.subscription_path(project_id, subscription_id)

    def callback(message):
        print(f"Received message: {message.data.decode('utf-8')}")
        message.ack()  # Acknowledge the message

    # Subscribe to the subscription
    streaming_pull_future = subscriber.subscribe(subscription_path, callback)
    print("Listening for messages on {}...\n".format(subscription_path))

    try:
        # Keep the main thread alive to listen to messages
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()

if __name__ == "__main__":
    project_id = "pub-sub-433616"
    subscription_id = "leraning-pull-sub"
    credentials_file = "pub-sub-key.json"

    pull_messages(project_id, subscription_id,credentials_file)
