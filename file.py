from flask import Flask, jsonify
import requests
import os

SHOP = os.environ["SHOP"]
CLIENT_ID = os.environ["CLIENT_ID"]
CLIENT_SECRET = os.environ["CLIENT_SECRET"]

app = Flask(__name__)


@app.route("/products")
def products():

    # Get access token
    token = requests.post(
        f"https://{SHOP}/admin/oauth/access_token",
        data={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        },
    ).json()["access_token"]

    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
    }

    query = """
    {
      products(first: 5) {
        nodes {
          title
          featuredImage {
            url
          }
          variants(first: 5) {
            nodes {
              id
              inventoryQuantity
            }
          }
        }
      }
    }
    """

    result = requests.post(
        f"https://{SHOP}/admin/api/2026-07/graphql.json",
        headers=headers,
        json={"query": query},
    ).json()

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
