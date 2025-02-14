| **Format Type** | **Description** | **Regex Pattern** | **Min Length** | **Max Length** |
|------------------|-----------------|-------------------|----------------|----------------|
| email | Validates email addresses | `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$` | 6 | 254 |
| phone | Validates phone numbers | `^\\+?(\\d{1,3})?[- .]?\\(?(\\d{3})\\)?[- .]?\\d{3}[- .]?\\d{4}$` | 10 | 20 |
| date | Validates dates (YYYY-MM-DD) | `^\\d{4}-\\d{2}-\\d{2}$` | 10 | 10 |
| time | Validates time (HH:MM:SS) | `^(0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$` | 8 | 8 |
| datetime | Validates datetime (YYYY-MM-DD HH:MM:SS) | `^\\d{4}-\\d{2}-\\d{2} (0[0-9]|1[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$` | 19 | 19 |
| url | Validates URLs | `^(https?:\\/\\/)?([\\da-z\\.-]+)\\.([a-z\\.]{2,6})([\\/\\w \\.-]*\\/*)?$` | 1 | 2048 |
| ipv4 | Validates IPv4 addresses | `^\\d{1,3}(\\.\\d{1,3}){3}$` | 7 | 15 |
| ipv6 | Validates IPv6 addresses | `^([0-9a-fA-F]{0,4}:){7}[0-9a-fA-F]{0,4}$` | 15 | 39 |
| credit_card | Validates credit card numbers | `^\\d{13,19}$` | 13 | 19 |
| ssn | Validates Social Security Numbers (USA) | `^\\d{3}-\\d{2}-\\d{4}$` | 11 | 11 |
| zip_code | Validates ZIP codes (USA) | `^\\d{5}(-\\d{4})?$` | 5 | 10 |
| username | Validates usernames | `^[a-zA-Z0-9_]{3,20}$` | 3 | 20 |
| password | Validates passwords (common rules) | `^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]{8,}$` | 8 | 20 |
| alphanumeric | Validates alphanumeric strings | `^[a-zA-Z0-9]+$` | 1 | N/A |
| hex_color | Validates hexadecimal color codes | `^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$` | 4 | 7 |
| isbn | Validates ISBN numbers | `^(?:ISBN-)?(?:\\d{9}X|\\d{10})$` | 9 | 10 |
| ean | Validates EAN-13 barcodes | `^\\d{13}$` | 13 | 13 |
| currency | Validates currency amounts | `^\\d{1,3}(?:,\\d{3})*\\.\\d{2}$` | 4 | 20 |
| percentage | Validates percentage values | `^([0-9]{1,2}|100)(\\.[0-9]{1,2})?$` | 1 | 5 |
| slug | Validates slugs (URL-friendly) | `^[a-z0-9-]+$` | 1 | N/A |
| uuid | Validates UUIDs | `^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$` | 36 | 36 |
