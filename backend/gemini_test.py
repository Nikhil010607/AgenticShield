from agents.orchestrator import investigate_message


message = """
URGENT! Your bank account will be blocked today.
Verify your account immediately by clicking this link.
Enter your OTP to confirm your identity.
"""

result = investigate_message(message)

print("\n========== AGENTSHIELD RESULT ==========\n")

print(result)