

```sh
from users.models import User
user = User.objects.create_user(
    email='staff1@example.com',
    password='securepassword123',
    username='staff1',
    role='Moderator'
)
print(user.role)  # Output: Moderator
