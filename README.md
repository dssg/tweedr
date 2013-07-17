# tweedr is Twitter for Disaster Response

Tweedr aims to develop machine learning and natural language processing tools to analyze social media created in response to a disaster. By enabling disaster relief agencies (e.g., [Red Cross](http://www.redcross.org/), [UN](http://www.un.org/en/), [FEMA](http://www.fema.gov/)) to quickly assimilate information coming in from various sources (generally, free text without a common format), so that they know what's damaged and where, this tool can help expedite on-site efforts.

Tweedr is a [Data Science for Social Good](http://dssg.io/) 2013 project.



## The problem: a flood

Disasters are chaotic, creating massive changes in the local environment and delivering damage stochastically throughout the affected area. In parallel, disasters often dramatically reduce the ability communication, by downing telephone lines and cutting power, wrecking roads and bridges, or otherwise debilitating effective transportation.

However, recovery efforts need the most up-to-date information available, to help them:

* Know what needs are most important to address.
    - Different areas will have different needs. One neighborhood might need help erecting temporary shelter, while another only needs food and water supplies.
* Decide what organizations are best suited to address different groups of needs.
* Plan recovery missions.
    - If some roads are impassable, the entire trip might need to be adjusted.

This lack of information means there is one more step between relief and the disaster victims, since the relief workers must perform their damage reconnaissance while out in the field, and return to headquarters to update and strategize their next venture.


## The solution: a flood of text

Social media can help with some of this. Mobile communication usually outlives landlines and other modes of communication, and in recent disasters, the volume of messages (SMSes and Tweets) sent from the disaster site is enormous. Effective use of this information requires immediately processing large amounts of natural text in a short amount of time. Currently, this means that Red Cross (or some other relief organization) workers have to sift through thousands of Tweets, SMSes, and calls, to extract useful information that will help them direct or carry out on-the-ground relief efforts.

NLP (Natural Language Processing) is one way to help with this processing. More general machine learning (ML) methods can help to geolocate tweets based on text and the social graph. The solution that we are developing as "tweedr" is primarily an API for adding ML-powered annotations, as well as a thin layer for viewing those annotations:

1. A pipeline that can process a stream of text (along with metadata) and produce useful annotations on top of that text.
2. An interface for effectively viewing these annotations in aggregate.

 
## The impact

Better-informed disaster relief providers can more efficiently address problems, e.g.,

* prioritize tasks
* deliver supplies
* route vehicles


---


## Description of a segment of labeled data

We have crowdsourced annotations of tweets sent during Hurricane Sandy

> ![Sandy picture](
http://i.huffpost.com/gadgets/slideshows/260253/slide_260253_1701938_free.jpg)

[Image credit: HuffPo](http://www.huffingtonpost.com/2012/10/30/hurricane-sandy-damage-photos-superstorm-unthinkable-aftermath_n_2044099.html)

and the Joplin tornado:

> ![Joplin wreckage](
http://d6673sr63mbv7.cloudfront.net/archive/x898210679/g00025800000000000071f2f594a33d9f9da0bc39ad9d7d1382bb008d99.jpg)

[Image credit: Joplin Globe](http://www.joplinglobe.com/local/x433426155/Widespread-damage-reported-after-tornado)

### Example (informative / caution / information source / donation / damage / other)

In one example of a target annotation domain, each tweet was assigned one of a number of categories:

* Casualties and damage
* Caution and advice
* Donations of money, goods or services
* People missing, found or seen
* Unknown
* Information source

For this type of data, our immediate goal is to replicate human annotations via machine learning.



## TODO

* Further exploration of statistical analyses and more sophisticated NLP tools.
* Find ways to evaluate the conclusions we come up with, by comparing to grounded data with quantitative reports of damage.
    - The human annotations are valuable, but having grounded data like Red Cross / FEMA damage reports might help us estimate how seriously to take our inferred mapping between Twitter and the real world.


## License

**To be determined.**
