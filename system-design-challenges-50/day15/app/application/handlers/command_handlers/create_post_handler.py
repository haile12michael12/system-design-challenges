from ....domain.entities.post import Post
from ....domain.value_objects.post_id import PostId
from ....domain.events.post_created import PostCreated
from ....application.commands.create_post import CreatePostCommand

class CreatePostHandler:
    def handle(self, command: CreatePostCommand) -> Post:
        # Create a new post entity
        post_id = PostId.new()
        post = Post(
            id=post_id,
            content=command.content,
            author=command.author
        )
        
        # Create and publish event
        event = PostCreated(
            post_id=post_id,
            content=command.content,
            author=command.author,
            created_at=None  # In a real implementation, this would be datetime.now()
        )
        
        # In a real implementation, we would publish the event here
        # event_publisher.publish(event)
        
        return post