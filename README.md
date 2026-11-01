# CodeAlpha Task Automation

Small Python automation utilities for the CodeAlpha internship task.

## Included automations

- Move `.jpg` and `.jpeg` files into another folder
- Extract unique email addresses from a text file
- Fetch and print the title of a fixed webpage

## Usage

```bash
python automation_tools.py move-jpg ./photos ./jpg_backup
python automation_tools.py extract-emails input.txt emails.txt
python automation_tools.py scrape-title https://example.com
python -m unittest discover -s tests -v
```
