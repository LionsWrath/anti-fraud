## Questions

### Explain the money flow and the information flow in the acquirer market and the role of the main players.

The main players are the Acquiring Banks, Issuing Banks, Card Networks, merchants and consumers.

- An *Acquiring Bank*, also called an acquirer, is an institution with authorization from the card networks to process transactions. Its objetives are to ensure transaction security and management of communications between credit and debit associations and business. The acquirer also takes responsability for the compromised transaction in the event of fraud or data breach.

- An *Issuing Bank*, or issuer, is an financial institution that provides credit and debit cards to customers. They are not the retainers of the Card Networks like Mastercard, Visa and American Express, but they issues cards in their behalf. It is the issuer responsability approve or deny customer applications and authentications, making sure there is enough funds for a transaction and guarantee payment even in cases of loss or damage.

- *Card Networks* institutions create the virtual payment infrastructure needed to facilitate transactions between merchants and issuers and charge merchants transaction fees. They also define where the cards are accepted, the business rules for purchases and act as a bridge between acquirers and issuers.

First, for any commerce start accepting credit and debit payments, it is needed an agreement with an acquirer. While, at the same time, an consumer wanting to buy at that commerce must have an a credit or debit card from an issuer.

Now, suppose that a customer fell in love with an product from the commerce and wants to make a payment. The following steps ensues for the *information and money flow*:

- The acquirer receives the payment request from the commerce;

- The acquirer then sends the payment request to the card networks that pass on the request to the issuer;

- The issuer now authenticates the consumer, makes a risk analysis and checks if there is enough funds to pay for the transaction;

- An approval code is sent back in the case that everything is ok;

- The transactions is approved, transferring the money from the issuer to the acquirer and from the acquirer to the merchant account;

- If an dispute from the consumer is needed, the issuer is responsible for the analysis and refund.

---
### Explain the difference between acquirer, sub-acquirer and payment gateway and how the flow explained in question 1 changes for these players.

- A *Payment Gateway* is a system responsible for the communication of payment data to acquirers, card brands and issuers banks. It integrates all of the payment chain players transactions in a single place;

- With a gateway, an *acquirer* can focus solely on processing payments, becaming highly specilized. It sends the informations to card brands and the issuing banks;

- An *sub-acquirer* is also a company that specializes in processing payments, but lack the autonomy to be a complete acquirer. It serves as a middle player between the acquirers and the merchant. Is usually used in small stores because of the low cost of implementation, dedicated anti-fraud system and easy integration, but the rates are usually higher per transaction.

Both the card networks and Issuing banks play similar roles as explained in Question 1.

---
### Explain what chargebacks are, how they differ from cancellations and what is their connection with fraud in the acquiring world.

*Chargebacks* are disputes of payments made from the consumer to the issuer to get his money back. They are linked with fraud as most of chargebacks are related to payments not known to the consumer. This dispute is received by the acquirer and redirected to the merchant. 

*Cancellations* happens when the merchant cancels the transaction, sending the data to the acquirer that redirect to the issuer of the consumer, cancelling the transaction. Cancellations can happen for many reasons and is usually not directly related with fraud.

Therefore, merchants with a high number of chargebacks can be considered suspicious, as there are many consumers disputing their purchases. This can be used by the acquirer to identity and deny these fraud prone payments on behalf of the customer without the need to involve the issuer.

## Exploratory Analysis 

### Analyze the data provided and present your conclusions (consider that all transactions are made using a mobile device).

The results of my analysis is available in the directory res in two versions. One is the analysis of the full dataset and the other is the analysis of only the rows that have no chargebacks. In this analysis, I used the following metrics:

 - Merchant Chargeback Rate;
 - Consumer Chargeback Rate;
 - Frequency of Purchases per User;
 - Value of Purchases per Consumer;
 - Value of Purchases per Merchant.

The *Merchant Chargeback Rate* and *Consumer Chargeback Rate* are the rate between the total number of purchases and the total number of chargebacks for the merchant and the consumer, respectively. For merchants, I considered a purchase suspicious when the rate is over 80% and the total number of purchases for the merchant is greater than 4 and for Consumer the rate must be over 50% and the total number of purchases more than 3 purchases. These numbers were chosen based on the presented data, but it must be different based on the context.

The *Frequency of Purchases per User* is given by the average and standard deviation based on the quantity of purchases per user and per day. So, for any given day, if the amount of purchases in the day goes over the amount that the user usually buys, the purchase is considered suspicious. This value is given by the calculation round( avg + stddev ) and the amount is based on a enumeration of the purchases for each day, where the purchases that go over the value are flagged. The standard deviation is used to consider the variation between purchases, as only the average is not precise enough.

Metrics *Value of Purchases per Consumer* and *Value of Purchases per Merchant* are based on the average value of the purchases related to the consumer and merchant, respectively. If the transaction amount of the purchase goes over two times the avg + stddev, the purchase is considered suspicious.

These analyses and the code related to them are available in the notebook Exploratory_Analysis.ipynb. Multiple metrics were used based on the assumption that one simple analysis is not enough to distinguish a fraudulent purchase from a legitimate one. So, multiple analysis are used and merged in the analysis available in the directory res. Suspicious activities will possibly trigger one or more flags. Note that the device_id is a metric by itself that shows when a device can be trusted and thus is present on the resulting dataset.

### In addition to the spreadsheet data, what other data would you look at to try to find patterns of possible frauds?

I would try to get more information on the merchants and what type of items they sell, for what price. With this, is possible to build a profile that can be used to cluster different types of stores and price tags. At the same time, the same can be done on the consumer side, categorizing how consumers spend their money. Between these categories, there would be the categories of known fraudulent merchants and consumers.

Moreover, extensive personal documentation validation is interesting to have a good foundation for data analysis. Merchants must use good digital signatures that can be easily verified by the system, while the same time information about the transaction network and IP can be considered, mainly for the digital stores and consumers, and verified against known informations about locations. There are limits to how much information about networks can be trusted though, as there are many ways of masking these.

As mobile devices were being used, GPS information is a great option to track positions and validate purchases, but again, most dedicated fraudulent merchant or consumers will know how to mask these informations with a VPN. A face photo is also an interesting way to identify people trying to face authentication, as discussed in the interview. If an photo or fake images are being used there must exist ways to identify these cases.
