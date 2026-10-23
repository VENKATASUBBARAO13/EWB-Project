# AWS VPC Peering Project — EWB

A hands-on AWS networking project demonstrating private communication between two VPCs using VPC peering, reciprocal route tables, security groups, and a bastion host.

> **Student details:** Fill in your full name and batch in the report before submission. The repository is public; do not upload private keys, passwords, AWS credentials, or tokens.

## Architecture diagram

![AWS VPC Peering Architecture](docs/architecture.svg)

**AWS Region:** US East (N. Virginia) — `us-east-1`

## Actual observed environment

| Resource | Actual CIDR / IP | Resource ID |
|---|---|---|
| VPC A | `10.10.0.0/16` | `vpc-094290dd996bdde79` |
| VPC B | `10.20.0.0/16` | `vpc-05463d53d9e3da06c` |
| VPC A public subnet | `10.10.1.0/24` | `subnet-0bca7727144ff4450` |
| VPC A private subnet | `10.10.2.0/24` | `subnet-08c38e5c7cf56cf16` |
| VPC B private subnet | `10.20.1.0/24` | `subnet-034834e10587f4b19` |
| Bastion | Private `10.10.1.10`, public `32.192.245.103` | `i-080bd656190adfe0c` |
| App-A | `10.10.2.108`, no public IPv4 observed | `i-005788d06eff77db3` |
| App-B | `10.20.1.226`, no public IPv4 observed | `i-03eb8ec8840385621` |
| VPC peering | Observed Active | `pcx-0cf7c6b7b06ee3eeb` |

The workbook's sample IPs differed from AWS-assigned App-A and App-B IPs. This repository uses the actual addresses observed during the lab.

## Route tables

| Route table | Destination | Target |
|---|---|---|
| `ewb-rt-a-public` (`rtb-0bffd516469dc9220`) | `10.10.0.0/16` | `local` |
| | `0.0.0.0/0` | Internet Gateway |
| | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-a-private` (`rtb-0df315a397a97459a`) | `10.10.0.0/16` | `local` |
| | `10.20.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |
| `ewb-rt-b-private` (`rtb-0e04e73e930ddf38c`) | `10.20.0.0/16` | `local` |
| | `10.10.0.0/16` | `pcx-0cf7c6b7b06ee3eeb` |

## Validation results

| Test | Observed result |
|---|---|
| SSH from laptop to bastion | Successful |
| SSH to App-B through bastion using SSH ProxyCommand | Successful shell on `ip-10-20-1-226` |
| App-A `10.10.2.108` → App-B `10.20.1.226` | 4 replies, 0% packet loss |
| App-B `10.20.1.226` → App-A `10.10.2.108` | 4 replies, 0% packet loss |
| Controlled ICMP rule-removal test | 100% packet loss while the App-B inbound ICMP Echo Request rule was removed |
| Recovery | 4 replies, 0% packet loss after the rule was restored |

## Traffic explanation

- App-A sends traffic to `10.20.1.226` through `10.20.0.0/16 → pcx-0cf7c6b7b06ee3eeb` in the private route table.
- VPC B returns traffic to `10.10.0.0/16` via the same peering connection.
- The bastion's public route table includes a peering route for `10.20.0.0/16`; SSH traffic to App-B uses its private IP.
- Keep the PEM key on the laptop. Do not upload it into this repository.

## Project report

See [`report/PROJECT_REPORT.md`](report/PROJECT_REPORT.md) for implementation notes, evidence status, lessons learned, and cleanup instructions.

## All screenshots

The complete screenshot set is stored in the `Screenshots/` folder. Expand this section to view the screenshots inline.

<details>
<summary>Open screenshot gallery (85 images)</summary>

![Screenshot 001: 079_reverse_ping_app_b_to_app_a](Screenshots/079_reverse_ping_app_b_to_app_a.webp)

![Screenshot 002: 080_controlled_failure_and_recovery](Screenshots/080_controlled_failure_and_recovery.webp)

![Screenshot 003: 081_peering_active](Screenshots/081_peering_active.webp)

![Screenshot 004: 082_ssh_app_b_via_bastion](Screenshots/082_ssh_app_b_via_bastion.webp)

![Screenshot 005: 083_vpc_a_public_routes](Screenshots/083_vpc_a_public_routes.webp)

![Screenshot 006: 084_vpc_b_private_routes](Screenshots/084_vpc_b_private_routes.webp)

![Screenshot 007: 085_network_configuration](Screenshots/085_network_configuration.webp)

![Screenshot 008: Screenshot 2026-10-23 111807](Screenshots/Screenshot 2026-10-23 111807.png)

![Screenshot 009: Screenshot 2026-10-23 112651](Screenshots/Screenshot 2026-10-23 112651.png)

![Screenshot 010: Screenshot 2026-10-23 112711](Screenshots/Screenshot 2026-10-23 112711.png)

![Screenshot 011: Screenshot 2026-10-23 113135](Screenshots/Screenshot 2026-10-23 113135.png)

![Screenshot 012: Screenshot 2026-10-23 113334](Screenshots/Screenshot 2026-10-23 113334.png)

![Screenshot 013: Screenshot 2026-10-23 113729](Screenshots/Screenshot 2026-10-23 113729.png)

![Screenshot 014: Screenshot 2026-10-23 114314](Screenshots/Screenshot 2026-10-23 114314.png)

![Screenshot 015: Screenshot 2026-10-23 114335](Screenshots/Screenshot 2026-10-23 114335.png)

![Screenshot 016: Screenshot 2026-10-23 114355](Screenshots/Screenshot 2026-10-23 114355.png)

![Screenshot 017: Screenshot 2026-10-23 115317](Screenshots/Screenshot 2026-10-23 115317.png)

![Screenshot 018: Screenshot 2026-10-23 115810](Screenshots/Screenshot 2026-10-23 115810.png)

![Screenshot 019: Screenshot 2026-10-23 115919](Screenshots/Screenshot 2026-10-23 115919.png)

![Screenshot 020: Screenshot 2026-10-23 120341](Screenshots/Screenshot 2026-10-23 120341.png)

![Screenshot 021: Screenshot 2026-10-23 121007](Screenshots/Screenshot 2026-10-23 121007.png)

![Screenshot 022: Screenshot 2026-10-23 121108](Screenshots/Screenshot 2026-10-23 121108.png)

![Screenshot 023: Screenshot 2026-10-23 121123](Screenshots/Screenshot 2026-10-23 121123.png)

![Screenshot 024: Screenshot 2026-10-23 121908](Screenshots/Screenshot 2026-10-23 121908.png)

![Screenshot 025: Screenshot 2026-10-23 122315](Screenshots/Screenshot 2026-10-23 122315.png)

![Screenshot 026: Screenshot 2026-10-23 122332](Screenshots/Screenshot 2026-10-23 122332.png)

![Screenshot 027: Screenshot 2026-10-23 122344](Screenshots/Screenshot 2026-10-23 122344.png)

![Screenshot 028: Screenshot 2026-10-23 122540](Screenshots/Screenshot 2026-10-23 122540.png)

![Screenshot 029: Screenshot 2026-10-23 122555](Screenshots/Screenshot 2026-10-23 122555.png)

![Screenshot 030: Screenshot 2026-10-23 122635](Screenshots/Screenshot 2026-10-23 122635.png)

![Screenshot 031: Screenshot 2026-10-23 122744](Screenshots/Screenshot 2026-10-23 122744.png)

![Screenshot 032: Screenshot 2026-10-23 123423](Screenshots/Screenshot 2026-10-23 123423.png)

![Screenshot 033: Screenshot 2026-10-23 123637](Screenshots/Screenshot 2026-10-23 123637.png)

![Screenshot 034: Screenshot 2026-10-23 124754](Screenshots/Screenshot 2026-10-23 124754.png)

![Screenshot 035: Screenshot 2026-10-23 125251](Screenshots/Screenshot 2026-10-23 125251.png)

![Screenshot 036: Screenshot 2026-10-23 125632](Screenshots/Screenshot 2026-10-23 125632.png)

![Screenshot 037: Screenshot 2026-10-23 125901](Screenshots/Screenshot 2026-10-23 125901.png)

![Screenshot 038: Screenshot 2026-10-23 130009](Screenshots/Screenshot 2026-10-23 130009.png)

![Screenshot 039: Screenshot 2026-10-23 130029](Screenshots/Screenshot 2026-10-23 130029.png)

![Screenshot 040: Screenshot 2026-10-23 130335](Screenshots/Screenshot 2026-10-23 130335.png)

![Screenshot 041: Screenshot 2026-10-23 130643](Screenshots/Screenshot 2026-10-23 130643.png)

![Screenshot 042: Screenshot 2026-10-23 130738](Screenshots/Screenshot 2026-10-23 130738.png)

![Screenshot 043: Screenshot 2026-10-23 130927](Screenshots/Screenshot 2026-10-23 130927.png)

![Screenshot 044: Screenshot 2026-10-23 131026](Screenshots/Screenshot 2026-10-23 131026.png)

![Screenshot 045: Screenshot 2026-10-23 131234](Screenshots/Screenshot 2026-10-23 131234.png)

![Screenshot 046: Screenshot 2026-10-23 131443](Screenshots/Screenshot 2026-10-23 131443.png)

![Screenshot 047: Screenshot 2026-10-23 131553](Screenshots/Screenshot 2026-10-23 131553.png)

![Screenshot 048: Screenshot 2026-10-23 131724](Screenshots/Screenshot 2026-10-23 131724.png)

![Screenshot 049: Screenshot 2026-10-23 131827](Screenshots/Screenshot 2026-10-23 131827.png)

![Screenshot 050: Screenshot 2026-10-23 132141](Screenshots/Screenshot 2026-10-23 132141.png)

![Screenshot 051: Screenshot 2026-10-23 132252](Screenshots/Screenshot 2026-10-23 132252.png)

![Screenshot 052: Screenshot 2026-10-23 132346](Screenshots/Screenshot 2026-10-23 132346.png)

![Screenshot 053: Screenshot 2026-10-23 132403](Screenshots/Screenshot 2026-10-23 132403.png)

![Screenshot 054: Screenshot 2026-10-23 132424](Screenshots/Screenshot 2026-10-23 132424.png)

![Screenshot 055: Screenshot 2026-10-23 132711](Screenshots/Screenshot 2026-10-23 132711.png)

![Screenshot 056: Screenshot 2026-10-23 133008](Screenshots/Screenshot 2026-10-23 133008.png)

![Screenshot 057: Screenshot 2026-10-23 133027](Screenshots/Screenshot 2026-10-23 133027.png)

![Screenshot 058: Screenshot 2026-10-23 133139](Screenshots/Screenshot 2026-10-23 133139.png)

![Screenshot 059: Screenshot 2026-10-23 133249](Screenshots/Screenshot 2026-10-23 133249.png)

![Screenshot 060: Screenshot 2026-10-23 133314](Screenshots/Screenshot 2026-10-23 133314.png)

![Screenshot 061: Screenshot 2026-10-23 133426](Screenshots/Screenshot 2026-10-23 133426.png)

![Screenshot 062: Screenshot 2026-10-23 133450](Screenshots/Screenshot 2026-10-23 133450.png)

![Screenshot 063: Screenshot 2026-10-23 133624](Screenshots/Screenshot 2026-10-23 133624.png)

![Screenshot 064: Screenshot 2026-10-23 133748](Screenshots/Screenshot 2026-10-23 133748.png)

![Screenshot 065: Screenshot 2026-10-23 134332](Screenshots/Screenshot 2026-10-23 134332.png)

![Screenshot 066: Screenshot 2026-10-23 134354](Screenshots/Screenshot 2026-10-23 134354.png)

![Screenshot 067: Screenshot 2026-10-23 134413](Screenshots/Screenshot 2026-10-23 134413.png)

![Screenshot 068: Screenshot 2026-10-23 134433](Screenshots/Screenshot 2026-10-23 134433.png)

![Screenshot 069: Screenshot 2026-10-23 134548](Screenshots/Screenshot 2026-10-23 134548.png)

![Screenshot 070: Screenshot 2026-10-23 134631](Screenshots/Screenshot 2026-10-23 134631.png)

![Screenshot 071: Screenshot 2026-10-23 134645](Screenshots/Screenshot 2026-10-23 134645.png)

![Screenshot 072: Screenshot 2026-10-23 135005](Screenshots/Screenshot 2026-10-23 135005.png)

![Screenshot 073: Screenshot 2026-10-23 135202](Screenshots/Screenshot 2026-10-23 135202.png)

![Screenshot 074: Screenshot 2026-10-23 135442](Screenshots/Screenshot 2026-10-23 135442.png)

![Screenshot 075: Screenshot 2026-10-23 135717](Screenshots/Screenshot 2026-10-23 135717.png)

![Screenshot 076: Screenshot 2026-10-23 135809](Screenshots/Screenshot 2026-10-23 135809.png)

![Screenshot 077: Screenshot 2026-10-23 135944](Screenshots/Screenshot 2026-10-23 135944.png)

![Screenshot 078: Screenshot 2026-10-23 140030](Screenshots/Screenshot 2026-10-23 140030.png)

![Screenshot 079: Screenshot 2026-10-23 140059](Screenshots/Screenshot 2026-10-23 140059.png)

![Screenshot 080: Screenshot 2026-10-23 140351](Screenshots/Screenshot 2026-10-23 140351.png)

![Screenshot 081: Screenshot 2026-10-23 140519](Screenshots/Screenshot 2026-10-23 140519.png)

![Screenshot 082: Screenshot 2026-10-23 140549](Screenshots/Screenshot 2026-10-23 140549.png)

![Screenshot 083: Screenshot 2026-10-23 140650](Screenshots/Screenshot 2026-10-23 140650.png)

![Screenshot 084: Screenshot 2026-10-23 140725](Screenshots/Screenshot 2026-10-23 140725.png)

![Screenshot 085: Screenshot 2026-10-23 140832](Screenshots/Screenshot 2026-10-23 140832.png)

</details>

## Before final submission

- Add the student's full name and batch.
- Verify all resource IDs and route associations in the live AWS Console.
- Capture cleanup evidence after the lab resources have actually been deleted.
- Ensure the bastion SSH inbound rule is restricted to your current public IPv4 `/32`; do not leave SSH open to `0.0.0.0/0`.
