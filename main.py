from discord import SyncWebhook
import discord
import requests
import os


# Configuration variables
facts_api_limit = "1"
facts_api_url = "https://api.api-ninjas.com/v1/facts?limit="
facts_api_key = os.environ["FACTS_API_KEY"]
discord_webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

# Call the fun fact API and return a list of facts
def get_fun_facts(limit):
    print("INFO: Calling Fun fact API")
    headers = {"X-Api-Key": facts_api_key}
    response = requests.get(f'{facts_api_url}{limit}', headers=headers)
    facts = []
    if response.ok:
        for fact in response.json():
            facts.append(fact["fact"])
        print(f'SUCCESS: Fun fact API request succeeded with status code {response.status_code}')
    else:
        print(f'ERROR: Fun fact API request failed with status code {response.status_code}')
    return facts

# Post fun facts to Discord webhook
def post_discord_webhook(facts):
    print("INFO: Posting to Discord webhook")
    webhook = SyncWebhook.from_url(discord_webhook_url)
    embed = discord.Embed(color=2695771)
    for i, fact in enumerate(facts):
        if len(facts) == 1:
            field_name = "Fun Fact"
        else:
            field_name = f'Fun Fact #{i + 1}'
        embed.add_field(name=field_name, value=fact, inline=False)
    webhook.send(embed=embed)
    print("SUCCESS: Posted to Discord webhook")

def main():
    facts = get_fun_facts(facts_api_limit)
    post_discord_webhook(facts)

if __name__ == "__main__":
    main()
