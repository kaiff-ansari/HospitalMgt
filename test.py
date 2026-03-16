from blockchain.hashservice import generate_hash


privateData = {
    "id" : 1,
    "name" : "kaif",
    "email" : "kaif@123gmail.com"
}

print(generate_hash(privateData))