#pip install mcp
from mcp.server.fastmcp import FastMCP
from tools import GmailTool 
import sys

# Ensure proper encoding for stdout and stderr
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# Initialize the MCP server and the Gmail tool
mcp = FastMCP('GmailAssistant')
tool = GmailTool()

@mcp.tool()
def create_draft(to: str, subject: str, body: str) -> str:
    """
    Creates a draft email with a recipient, subject, and body.
    
    Args:
        to (str): The email address of the recipient.
        subject (str): The subject line of the email.
        body (str): The main content of the email.
    """
    result = tool.create_draft(to=to, subject=subject, body=body)
    return result

@mcp.tool()
def send_email(to: str, subject: str, body: str) -> str:
    """
    Sends an email with a recipient, subject, and body.
    
    Args:
        to (str): The email address of the recipient.
        subject (str): The subject line of the email.
        body (str): The main content of the email.
    """
    result = tool.send_email(to=to, subject=subject, body=body)
    return result

def main():
    """Runs the FastMCP server."""
    mcp.run() 
    print("SERVER IS RUNNING")
if __name__ == "__main__":
    main()
