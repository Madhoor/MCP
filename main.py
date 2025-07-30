from mcp.server.fastmcp import FastMCP

#TODO prompt based 
# create a server 
mcp = FastMCP("first-one")
# whatev
@mcp.tool()
def multiply(a:int,b:int):
    """Multiply 2 numbers """ 
    return a*b

# @mcp.prompt()


# Example of a prompt function (uncomment and implement as needed)
@mcp.prompt()
def prompt(user_query: str) -> str:
    """
    Processes natural language queries and can potentially
    route them to other tools.
    """
    user_query = user_query.lower()
    if "multiply" in user_query:
        # Simple example: try to extract numbers and call multiply
        try:
            parts = user_query.split()
            num1 = int(parts[parts.index("multiply") + 1])
            num2 = int(parts[parts.index("multiply") + 2])
            result = multiply(num1, num2)
            return f"The product is: {result}"
        except (ValueError, IndexError):
            return "Please provide two numbers after 'multiply'."
    elif "add" in user_query:
        # Similar logic for addition
        pass # Implement extraction and call add()
    return f"I received your query: '{user_query}'. I don't have a specific tool for that yet."
# def prompt(string)


def main():
    print("Hello from first-server!")


if __name__ == "__main__":
    main()
    mcp.run()