print("================================")
print("       RazorResolve AI")
print("================================")

problem = input("\nDescribe your problem: ").lower()

if "settlement" in problem or "money" in problem or "payout" in problem:
    print("\nIssue: Settlement Problem")
    print("Possible Reason: Your settlement may be delayed or on hold.")
    print("Recommended Action: Check your settlement status and verification details.")

elif "refund" in problem:
    print("\nIssue: Refund Problem")
    print("Possible Reason: Your refund may still be processing.")
    print("Recommended Action: Check the refund status and transaction details.")

elif "kyc" in problem or "verification" in problem:
    print("\nIssue: KYC Problem")
    print("Possible Reason: Your KYC verification may be incomplete.")
    print("Recommended Action: Check your KYC status and required documents.")

elif "payment" in problem or "transaction" in problem:
    print("\nIssue: Payment Problem")
    print("Possible Reason: The payment may have failed due to a bank or payment issue.")
    print("Recommended Action: Check the payment status and failure reason.")

elif "account" in problem or "blocked" in problem or "restricted" in problem:
    print("\nIssue: Account Problem")
    print("Possible Reason: Your account may have a restriction or verification issue.")
    print("Recommended Action: Check your account status and notifications.")

else:
    print("\nIssue: Unable to identify")
    print("Recommended Action: Human review is required.")
