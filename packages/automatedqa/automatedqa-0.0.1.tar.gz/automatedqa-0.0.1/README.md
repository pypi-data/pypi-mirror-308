# Automated QA

```
python -m automatedqa https://tavos-dev.thalocan.com
```


```
self.enter("E-mail", 'thalocanadministrator@tavos.com')
self.enter("Password", 'Pass@2023')
self.click("Login")

self.click("Consensus")
self.click("New Consensus")
self.enter("Study Name", "Study 001")
self.enter("Name", "Consensus 001")
self.enter("Date for Part I", '12/10/2024 15:00')
self.enter("Interval days to Part II (business day)", "1")
self.enter("Days to Complete", "2")
self.enter("Severity", "Severity 001")
self.click("Add Severity")
self.enter("Severity", "Severity 002")
self.click("Next")

```