# GitHub Repository Secrets Setup

To enable automatic deployment with GitHub Actions, set up the following secrets in your GitHub repository:

1. Go to your GitHub repository settings
2. Click on "Secrets and variables" → "Actions"
3. Add the following secrets:

## Required Secrets

| Secret Name | Description |
|-------------|-------------|
| SSH_PRIVATE_KEY | Your private SSH key to access the VPS |
| SSH_KNOWN_HOSTS | The known hosts entry for your VPS |
| SSH_USER | Username for SSH access to your VPS |
| SSH_HOST | Your VPS hostname or IP address |
| DEPLOY_PATH | Path on the VPS where to deploy the app (e.g., /home/user/radhaapi) |

## How to Generate SSH Keys

If you don't have an SSH key pair yet:

```bash
# Generate new SSH key
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"

# Copy public key to your VPS
ssh-copy-id user@your-vps-ip

# Get the known hosts entry
ssh-keyscan -t rsa your-vps-ip
```

Copy the contents of your private key file (~/.ssh/id_rsa) to the SSH_PRIVATE_KEY secret, and the output of the ssh-keyscan command to SSH_KNOWN_HOSTS.

## Security Notes

- Never commit your SSH keys or sensitive information to the repository
- Always use secrets for sensitive information
- Consider using a deployment key with limited access for added security
