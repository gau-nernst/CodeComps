# Shopee - I'm the Best Coder! Challenge 2019

The competition comprises of two rounds, each lasts for around 1h30min. Although I didn't win anything, I learnt a lot from this experience. The notebooks here are my attempt after the competition i.e. when I have unlimited time to think and write the code.

The task details are reproduced as below. All data sets and task materials are properties of Shopee Singapore.

## Round 2 - Fraud Detection

Fraudsters create fake transactions to boost sales/shop ratings. Fake transactions are defined as transactions where the buyer and seller are the same individual (in reality). To help Shopee tackle this issue, you are expected to detect these fake transactions from normal transactions. Sample data for transactions and users' details will be provided.

### Task

Find fake orders where the buyer and the seller are directly or indirectly linked, by any of the following links: Device, Credit Card, Bank Account.

Direct link: the buyer and the seller share the same details.
Indirect link: the buyer and the seller are not directly linked, but users who share the same details as them share details with one another:
e.g. buyer - user A - user B - user C - … - user Z - seller

__Basic Concepts__
-  Each userid represents a distinct user on Shopee.
- Each orderid represents a distinct transaction on Shopee.
- Device, Credit Card, Bank Account data is encrypted to preserve data privacy. Each distinct value represents a unique entity.

### Examples
__Example 1__ `orderid: 1955598428`, `buyer userid: 35545436`, `seller userid: 70763052`.

The buyer has this device: `/3TLpeou8xXsNxpACFFKr34Kqqwxiu5Hi1keJ6plk5E=`.
The seller also has this device: `/3TLpeou8xXsNxpACFFKr34Kqqwxiu5Hi1keJ6plk5E=`.
Therefore, we consider that the buyer and the seller are directly linked by device.

This order is a fraud order by definition.

__Example 2__ `orderid: 1953543830`, `buyer userid: 223406364`, `seller userid: 193350172`.

User `223406364` is directly linked to user `227839480` by sharing the same device `7q1zwUrfP8+09Z+EPh+YyNYTwxhHW7wfGuIFWhRE490=`.

User `227839480` is directly linked to user `193350172` by sharing the same device `IkGjfHwwIGYxZ4WkM30COPKkmALyJfSSODpNTTPuMyS=`.

Therefore, buyer (`userid: 223406364`) is indirectly linked to seller (`userid: 193350172`).
This order is a fraud order by definition.

### Submit Format
Two columns required:
- `orderid`
- `is_fraud`: assign value 1 if the order is fraud, otherwise 0.

### Input
`orders.csv`: It contains orders information. Columns: `[orderid, buyer_userid, seller_userid]`.

`devices.csv`: It contains devices used by the users. Each value represents a unique device. If two users use the same device, they are linked by device. Columns: `[userid, device]`.

`credit_cards.csv`: It contains credit cards used by the users. If two users use the same credit card, they are linked by credit card. Columns: `[userid, credit_card]`.

`bank_accounts.csv`: It contains bank accounts used by the users. If two users use the same bank account, they are linked by bank account. Columns: `[userid, bank_account]`.

### Output
Check each order and determine whether it is a fraud order.