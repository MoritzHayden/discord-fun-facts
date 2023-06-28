from discord import SyncWebhook
import discord
import requests
import os
import json


# Configuration variables
facts_api_url = "https://api.api-ninjas.com/v1/facts?limit=1"
facts_api_key = os.environ["FACTS_API_KEY"]
discord_webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

# Call the fun fact API and return a fact
def get_fun_fact():
    print("INFO: Calling Fun fact API")
    headers = {"X-Api-Key": facts_api_key}
    response = requests.get(f'{facts_api_url}', headers=headers)

    if response.ok:
        print(f'SUCCESS: Fun fact API request succeeded with status code {response.status_code}')
        return response.json()[0]["fact"]
    else:
        print(f'ERROR: Fun fact API request failed with status code {response.status_code}')
        return None

# Check if the fact is a duplicate
def is_duplicate_fact(fact):
    with open('history.json') as file:
        fact_history = json.loads(file.read())["history"]

    print(f'INFO: Fact in history: {fact in fact_history}')
    return fact in fact_history

# Add the fact to the history
def add_fact_to_history(fact):
    with open('history.json', 'r+', encoding='utf-8') as file:
        fact_history = json.loads(file.read())
        fact_history["history"].append(fact)
        file.seek(0)
        file.write(json.dumps(fact_history, ensure_ascii=False, indent=2))

# Post fun facts to Discord webhook
def post_discord_webhook(fact):
    print("INFO: Posting to Discord webhook")
    webhook = SyncWebhook.from_url(discord_webhook_url)
    embed = discord.Embed(color=2695771)
    embed.add_field(name='Did You Know?', value=fact, inline=False)
    webhook.send(embed=embed)
    print("SUCCESS: Posted to Discord webhook")

# Main function
def main():
    while(True):
        fact = get_fun_fact()
        if fact is not None:
            if not is_duplicate_fact(fact):
                add_fact_to_history(fact)
                post_discord_webhook(fact)
                break

if __name__ == "__main__":
    main()
