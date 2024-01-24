import requests
import os

# Cloudflare API credentials
api_token = ''
headers = {'Authorization': f'Bearer {api_token}', 'Content-Type': 'application/json'}

# Directory to save Terraform files
output_directory = 'terraform_files'
os.makedirs(output_directory, exist_ok=True)

# Fetch all zones (domains) from Cloudflare
def fetch_zones():
    url = 'https://api.cloudflare.com/client/v4/zones'
    response = requests.get(url, headers=headers)
    data = response.json()
    if not data.get('success'):
        raise ValueError(f"Failed to fetch zones: {data.get('errors')}")
    return data['result']

# Fetch DNS records for a specific zone
def fetch_dns_records(zone_id):
    url = f'https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records'
    response = requests.get(url, headers=headers)
    data = response.json()
    if not data.get('success'):
        raise ValueError(f"Failed to fetch DNS records for zone {zone_id}: {data.get('errors')}")
    return data['result']

# Generate Terraform configuration for a zone and its DNS records
def generate_terraform_config(zone, records):
    tf_content = f'resource "cloudflare_zone" "{zone["name"]}" {{\n  zone = "{zone["name"]}"\n}}\n\n'

    for record in records:
        tf_content += f'resource "cloudflare_record" "{zone["name"]}_{record["name"]}_{record["type"]}" {{\n'
        tf_content += f'  zone_id = cloudflare_zone.{zone["name"]}.id\n'
        tf_content += f'  name    = "{record["name"]}"\n'
        tf_content += f'  type    = "{record["type"]}"\n'
        tf_content += f'  value   = "{record["content"]}"\n'
        tf_content += f'  proxied = {str(record.get("proxied", False)).lower()}\n'
        tf_content += '}\n\n'
    
    return tf_content

# Main function to orchestrate the import
def main():
    try:
        zones = fetch_zones()
    except ValueError as e:
        print(e)
        return

    for zone in zones:
        try:
            records = fetch_dns_records(zone['id'])
        except ValueError as e:
            print(e)
            continue

        tf_config = generate_terraform_config(zone, records)
        
        with open(os.path.join(output_directory, f'{zone["name"]}.tf'), 'w') as file:
            file.write(tf_config)
        print(f'Terraform configuration for {zone["name"]} written to {output_directory}/{zone["name"]}.tf')

if __name__ == "__main__":
    main()
