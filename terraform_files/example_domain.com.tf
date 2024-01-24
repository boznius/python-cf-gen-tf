// example terraform domain file for records to be put into.
resource "cloudflare_zone" "example_domain.com" {
  zone = "example_domain.com"
}

resource "cloudflare_record" "example_domain.com_email.example_domain.com_CNAME" {
  zone_id = cloudflare_zone.example_domain.com.id
  name    = "email.example_domain.com"
  type    = "CNAME"
  value   = "eu.mailgun.org"
  proxied = false
}

resource "cloudflare_record" "example_domain.com_example_domain.com_CNAME" {
  zone_id = cloudflare_zone.example_domain.com.id
  name    = "example_domain.com"
  type    = "CNAME"
  value   = "obscure-tangerine.herokudns.com"
  proxied = false
}


