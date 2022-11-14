The following list conceptually groups all available indicators. Each indicator description links to all relevant metrics that are implemented in the toolbox. Each indicator is labelled with its level of observation: <span class="label contributor">contributor</span> <span class="label contribution">contribution</span> <span class="label initial-contribution">initial contribution</span>
 <span class="label thread">thread</span> <span class="label community">community</span>. Specialized indicators are marked with <span class="label specialized">specialized</span> and state which additional data is required.
 
Please refer to the [user guide](../guide) and the [examples](../examples) on how to [generate the indicators](../guide/indicators/#generating-indicator-values) or how to [set up a custom indicator](../guide/indicators/#defining-new-indicators).
 
## Status and reputation

<span class="label contributor">contributor</span>

#### Concept

Status and reputation refer to the standing of a collaborator in the community showing in the recognition and esteem received from other community members. Individuals with high status enjoy more trust which is an important foundation for knowledge sharing[^1] and commitment [2]. Also, the contributors' reputation influences their ability to garner attention and curiosity for their contributions [3] which are generally more positively evaluated [1]. 

#### Metrics

Possible metrics indicating status and reputation are the In-degree centrality [4] and the Average number of replies to initial contribution [5].

### In-degree centrality
 
- [``in-degree centrality``](../reference/pici/metrics/network/#pici.metrics.network.in_degree_centrality)
 
### Average number of replies to initial contribution
 
- [``avg number of replies``](../reference/pici/metrics/basic/#pici.metrics.basic.replies_to_initial_post)

[^1]:
Menon, T., & Blount, S. (2003). The messenger bias: A relational model of knowledge valuation. Research in Organizational Behavior, 25, 137-186.

[2] Bateman, P. J., Gray, P. H., & Butler, B. S. (2011). Research note—the impact of community commitment on participation in online communities. Information systems research, 22(4), 841-854.

[3] Yuan, X., Yang, S., & Wang, C. (2017, July). Lead user identification in online user innovation communities: A method based on random forest classification. In 2017 7th IEEE International Conference on Electronics Information and Emergency Communication (ICEIEC) (pp. 157-160). IEEE.

[4] Füller, J., Hutter, K., Hautz, J., & Matzler, K. (2014). User roles and contributions in innovation-contest communities. Journal of management information systems, 31(1), 273-308.

[5] Yuan, X., Yang, S., & Wang, C. (2017, July). Lead user identification in online user innovation communities: A method based on random forest classification. In 2017 7th IEEE International Conference on Electronics Information and Emergency Communication (ICEIEC) (pp. 157-160). IEEE.
 
## Expertise

<span class="label contributor">contributor</span>
 
#### Concept

Expertise refers to the competence of contributors to make outstanding contributions in their field of knowledge. If community members can draw on relevant expertise [1] and convey their knowledge to others [2] the collaborations are more likely to be innovative. The more expertise exists in knowledge domains, the more likely it can be recombined to generate new ideas [3]. 

#### Metrics

Measuring the existing product knowledge of contributors can be accomplished by matching their contributions against a predefined glossary [2] or by network-based ranking algorithms [4][5]. Further metrics that measure the depth of information utilization from knowledge domains already existing in the community can be developed through topic modelling [3].

### Product Knowledge (number of words used from a glossary)

TO DO 

### the number of times a topic of the uploaded idea appeared in the commented ideas 

TO DO

[1] Lüthje, C. (2004). Characteristics of innovating users in a consumer goods field: An empirical study of sport-related product consumers. Technovation, 24(9), 683-695.

[2] Marchi, G., Giachetti, C., & De Gennaro, P. (2011). Extending lead-user theory to online brand communities: The case of the community Ducati. Technovation, 31(8), 350-361.

[3] Resch, C., & Kock, A. (2021). The influence of information depth and information breadth on brokers’ idea newness in online maker communities. Research Policy, 50(8), 104142.

[4] Agichtein, E., Castillo, C., Donato, D., Gionis, A., & Mishne, G. (2008, February). Finding high-quality content in social media. In Proceedings of the 2008 international conference on web search and data mining (pp. 183-194).

[5] Zhang, J., Ackerman, M. S., & Adamic, L. (2007, May). Expertise networks in online communities: structure and algorithms. In Proceedings of the 16th international conference on World Wide Web (pp. 221-230).
 
## Experience

<span class="label contributor">contributor</span>

#### Concept

The contributors' experience evolves from continuous learning by observing the activities of other community members [1][2] or one's participation in the community [3][4]. Experience fosters the emergence of expertise but does not necessarily amount to it [4]. Increased familiarity with common formulations, needs, and values allows for a better information overview within the community [2] as well as an improved elaboration of contributions strengthening their credibility and persuasiveness [1][5]. Thus, the contributions of experienced contributors have a higher innovation potential [6][7]. 

#### Metrics

The most common experience metrics are the number of contributions [3][6][8][9][10][11] and the amount of time spent in the community [5][6][12]. More sophisticated metrics use network analysis to determine out-degree centrality [9] and topic modelling to determine the number of times a topic appeared in a contributor's previous ideas [2].
 
### Topic re-occurence

<span class="label initial-contribution">initial contribution</span>
 
"The number of times a topic of the uploaded idea appeared in previous own ideas".
 
[1] Resch, C., & Kock, A. (2020). The influence of information depth and information breadth on brokers’ idea newness in online maker communities. *Research Policy, 104142.* https://doi.org/10.1016/j.respol.2020.104142
 
### Previous knowledge domains

<span class="label initial-contribution">initial contribution</span>
 
"The number of different knowledge domains with which an individual engaged in previous own ideas"
 
[1] Resch, C., & Kock, A. (2020). The influence of information depth and information breadth on brokers’ idea newness in online maker communities. *Research Policy, 104142.* https://doi.org/10.1016/j.respol.2020.104142
 
### Tenure
 
<span class="label contributor">contributor</span>
 
TODO:would have to include data since forum inception..?!
 
- [``days since first contribution``](../reference/pici/metrics/basic/#pici.metrics.basic.days_since_first_contribution)
 
### Absolute contributions
 
<span class="label contributor">contributor</span>
 
Number of contributions, number of intial contributions.
 
- [``number of contributions``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_contributions)
- [``number of initial contributions``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_initial_contributions)

### Normalized contributions
 
<span class="label contributor">contributor</span>
 
Number of contributions, number of initial contributions; normalized by time spent in community / length of contribution / number of replies to initial contribution
 
- [``number of contributions``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_contributions)
- [``number of initial contributions``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_initial_contributions)
 
### Out-degree centrality
 
<span class="label contributor">contributor</span>

[1] Piezunka, H., & Dahlander, L. (2015). Distant search, narrow attention: How crowding alters organizations’ filtering of suggestions in crowdsourcing. Academy of Management Journal, 58(3), 856-880.

[2] Resch, C., & Kock, A. (2021). The influence of information depth and information breadth on brokers’ idea newness in online maker communities. Research Policy, 50(8), 104142.

[3] Beretta, M. (2019). Idea selection in web‐enabled ideation systems. Journal of Product Innovation Management, 36(1), 5-23.

[4] Chan, K. W., Li, S. Y., Ni, J., & Zhu, J. J. (2021). What feedback matters? The role of experience in motivating crowdsourcing innovation. Production and Operations Management, 30(1), 103-126.

[5] Li, M., Kankanhalli, A., & Kim, S. H. (2016). Which ideas are more likely to be implemented in online user innovation communities? An empirical analysis. Decision Support Systems, 84, 28-40.

[6] Bayus, B. L. (2013). Crowdsourcing new product ideas over time: An analysis of the Dell IdeaStorm community. Management science, 59(1), 226-244.

[7] Simonton, D. K. (2003). Scientific creativity as constrained stochastic behavior: the integration of product, person, and process perspectives. Psychological bulletin, 129(4), 475.

[8] Fuger, S., Schimpf, R., Füller, J., & Hutter, K. (2017). User roles and team structures in a crowdsourcing community for international development–a social network perspective. Information Technology for Development, 23(3), 438-462.

[9] Füller, J., Hutter, K., Hautz, J., & Matzler, K. (2014). User roles and contributions in innovation-contest communities. Journal of management information systems, 31(1), 273-308.

[10] Jensen, M. B., Hienerth, C., & Lettl, C. (2014). Forecasting the commercial attractiveness of user‐generated designs using online data: An empirical study within the LEGO user community. Journal of Product Innovation Management, 31, 75-93.

[11] Lee, H., & Suh, Y. (2016). Who creates value in a user innovation community? A case study of MyStarbucksIdea. com. Online Information Review.

[12] Hoornaert, S., Ballings, M., Malthouse, E. C., & Van den Poel, D. (2017). Identifying new product ideas: waiting for the wisdom of the crowd or screening ideas in real time. Journal of Product Innovation Management, 34(5), 580-597.
 
## Diversity of contributions

<span class="label contributor">contributor</span>

#### Concept

Online communities are commonly divided into multiple sub-forums that allow the members to deal with different topics. By engaging in multiple topics, contributors can accumulate a more comprehensive and multifaceted compilation of knowledge enhancing their innovativeness [1]. 

#### Metrics

The diversity of contributions can be reflected in how many knowledge domains and external resources were drawn from, as well as the extent to which the content differs from other ideas in the community [2]. Also, the diversity of ideas [1][3] and past commenting activity [3] can be quantified by an entropy measure over categories [3] or by counting the number of categories [1]. 

### Sub-forum diversity
 
The diversity of a contributor's contributions in regard to which sub-forum they were made to. Diversity is either defined as a) *total number of different sub-forums*, or b) *the entropy of contributing behavior in gerade to sub-forum "classes"*. Each metric is defined for both 1) *all contributions*, and 2) *inital contributions* only.
 
- [``number of sub-forums contributed to``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_contributions)
- [``number of sub-forums made initial contributions to``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_contributions)
- [``entropy of sub-forums contributed to``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_contributions)
- [``entropy of sub-forums made inital contributions to``](../reference/pici/metrics/basic/#pici.metrics.basic.number_of_contributions)

### Links to external resources

TODO

### Content distance

TODO

[1] Jensen, M. B., Hienerth, C., & Lettl, C. (2014). Forecasting the commercial attractiveness of user‐generated designs using online data: An empirical study within the LEGO user community. Journal of Product Innovation Management, 31, 75-93.

[2] Resch, C., & Kock, A. (2021). The influence of information depth and information breadth on brokers’ idea newness in online maker communities. Research Policy, 50(8), 104142.

[3] Bayus, B. L. (2013). Crowdsourcing new product ideas over time: An analysis of the Dell IdeaStorm community. Management science, 59(1), 226-244.
 
## Providing assistance

<span class="label contributor">contributor</span>

#### Concept

Providing Assistance refers to the support of community members in the development and processing of ideas [1]. Mutual support raises the contributors' activity level which can increase their experience and expertise [2]. Higher expertise can increase willingness to help [3], thus promoting collaborative innovation processes [4][5]. Possible indicators capturing assistance provision are initiator helpfulness and originality. 

#### Metrics

Possible indicators capturing assistance provision are initiator helpfulness and originality. Initiator helpfulness can be measured via the percentage of posts a user contributes that he/she did not start [4], as well as the number of time frames a user contributed something [5]. A more sophsiticated metric measuring the originality in assistance is the average newness of previous ideas based on topic modelling [6].

### Initiator helpfulness

- contribution regularity (done)
- top commenter (?)
- comment frequency in foreign threads (TODO)

### Initiator originality

- average newness of previous ideas based on topic model (TODO, difficult)

[1] Franke, N., & Shah, S. (2003). How communities support innovative activities: an exploration of assistance and sharing among end-users. Research policy, 32(1), 157-178.

[2] Füller, J., Jawecki, G., & Mühlbacher, H. (2007). Innovation creation by online basketball communities. Journal of business research, 60(1), 60-71.

[3] Bilgram, V., Brem, A., & Voigt, K. I. (2008). User-centric innovations in new product development—Systematic identification of lead users harnessing interactive and collaborative online-tools. International journal of innovation management, 12(03), 419-458.

[4] Grosse, M., Pohlisch, J., & Korbel, J. J. (2018). Triggers of collaborative innovation in online user communities. Journal of Open Innovation: Technology, Market, and Complexity, 4(4), 59.

[5] Marchi, G., Giachetti, C., & De Gennaro, P. (2011). Extending lead-user theory to online brand communities: The case of the community Ducati. Technovation, 31(8), 350-361.

[6] Resch, C., & Kock, A. (2021). The influence of information depth and information breadth on brokers’ idea newness in online maker communities. Research Policy, 50(8), 104142.
 
## Past success

<span class="label contributor">contributor</span>

#### Concept

Past success refers to the community members' accomplishments of generating innovative or user-value-added contributions. Users who have already been successful are more likely to make high-quality contributions again [1][2] since they had the chance to learn how to develop highly accepted ideas [3][4]. However, if learned success behaviors stiffen, cognitive fixation risks limiting creativity in generating new ideas [5][6].

#### Metrics

Past success can be measured via the number of past contributions that were recognized as successful [1][4][7]. In the context of idea communities, a possible success metric is the adoption rate of suggested ideas over the total number of all suggestions made by the contributor [2].  

[1] Hoornaert, S., Ballings, M., Malthouse, E. C., & Van den Poel, D. (2017). Identifying new product ideas: waiting for the wisdom of the crowd or screening ideas in real time. Journal of Product Innovation Management, 34(5), 580-597.

[2] Li, M., Kankanhalli, A., & Kim, S. H. (2016). Which ideas are more likely to be implemented in online user innovation communities? An empirical analysis. Decision Support Systems, 84, 28-40.

[3] Deichmann, D., & Ende, J. V. D. (2014). Rising from failure and learning from success: The role of past experience in radical initiative taking. Organization Science, 25(3), 670-690.

[4] Ma, J., Lu, Y., & Gupta, S. (2019). User innovation evaluation: Empirical evidence from an online game community. Decision Support Systems, 117, 113-123.

[5] Bayus, B. L. (2013). Crowdsourcing new product ideas over time: An analysis of the Dell IdeaStorm community. Management science, 59(1), 226-244.

[6] Dahl, D. W., & Moreau, P. (2002). The influence and value of analogical thinking during new product ideation. Journal of marketing research, 39(1), 47-60.

[7] Beretta, M. (2019). Idea selection in web‐enabled ideation systems. Journal of Product Innovation Management, 36(1), 5-23.
 
## Network position
 
### Fuger-role
 
<span class="label contributor">contributor</span>
 
#### Concept
 
Contributors can be classified by how much they engage in discussions by commenting (reacting to initial contributions), versus how much they initially contribute themselves. [1] distinguish the four classes "collaborator", "contributor", "allrounder", and "passive user". For example, "collaborators" are contributors that are often involved in discussions, but do not often contribute own ideas. Their contributions were found to be of higher quality in a crowdsourcing context [1].
 
[1] constructed a social network of "actor-to-actor relationships" "based on comments written on ideas". They used in-degree (comments received) and out-degree (comments given), as well as the number of contributions (ideas, stories, etc.) to determine user clusters (k-means) and users' roles. Qualitatively, their classification/clustering results can be summarized as:
 
|              | In-degree | Out-degree | Contributions |
|--------------|-----------|------------|---------------|
| Collaborator | High      | High       | Low           |
| Contributor  | High      | High       | High          |
| Allrounder   | Medium    | Medium     | Medium        |
| Passive user | Low       | Low        | Low           |
 
#### Metrics
 
This group of metrics assigns one of the four classes to each contributor: It uses the co-contribution network to determine each user's number of "received" and "given" comments (weighted in- and out-degree). In- and out-degree and number of initial posts form the basis for a community-level clustering with a fixed number of four clusters. Cluster centers are then ranked, and cluster labels assigned according to the table above. 
 
*Implemented:*
 
Contributor:

- [``fuger-role``](../reference/pici/metrics/basic/#pici.metrics.network.fuger_role)
 
Topic:

- [``first post by collaborator``](../reference/pici/metrics/basic/#pici.metrics.network.first_post_fuger_role)
- [``first post by contributor``](../reference/pici/metrics/basic/#pici.metrics.network.first_post_fuger_role)
- [``first post by allrounder``](../reference/pici/metrics/basic/#pici.metrics.network.first_post_fuger_role)
- [``first post by passive user``](../reference/pici/metrics/basic/#pici.metrics.network.first_post_fuger_role)
 
[1] Fuger, S., Schimpf, R., Füller, J., & Hutter, K. (2017). User roles and team structures in a crowdsourcing community for international development - a social  network perspective. *Information Technology for Development, 23(3)*, 438-462. https://doi.org/10.1080/02681102.2017.1353947
 
### Fueller-role
 
<span class="label contributor">contributor</span>
 
#### Concept
 
In the context of innovation-contest communities, [1] define six contributor roles by qualitative evaluation of contributor clusters, formed based on contribution patterns. Contribution patterns are defined on a co-contribution network using in-degree (comments directed towards contributor), out-degree (comments made by contributor), and number of contributions by contributor. The roles are labelled *socializer*, *idea generator*, *master*, *efficient contributor*, *passive idea generator*, and *passive commentator* (see table below). They find that  
 
|                        | In-degree | Out-degree | Contributions |
|------------------------|-----------|------------|---------------|
| Socializer             | Low       | High       | Low           |
| Idea generator         | Medium    | Low        | High          |
| Master                 | Very high | High       | Very high     |
| Efficient contributor  | Medium    | Low        | Medium        |
| Passive idea generator | None      | None       | Very low      |
| Passive commentator    | None      | Very low   | None          |
 
*Implemented:*
 
Contributor:

- [``fueller-role``](../reference/pici/metrics/basic/#pici.metrics.network.fueller_role)
 
Topic:

- [``first post by socializer``](../reference/pici/metrics/network/#pici.metrics.network.first_post_fuger_role)
- [``first post by idea generator``](../reference/pici/metrics/network/#pici.metrics.network.first_post_fuger_role)
- [``first post by master``](../reference/pici/metrics/network/#pici.metrics.network.first_post_fuger_role)
- [``first post by efficient contributor``](../reference/pici/metrics/network/#pici.metrics.network.first_post_fuger_role)
- [``first post by passive idea generator``](../reference/pici/metrics/network/#pici.metrics.network.first_post_fuger_role)
- [``first post by passive commentator``](../reference/pici/metrics/network/#pici.metrics.network.first_post_fuger_role)

[1] Füller, J., Hutter, K., Hautz, J., & Matzler, K. (2014). User Roles and Contributions in Innovation-Contest Communities. *Journal of Management Information Systems, 31(1),* 273–308. https://doi.org/10.2753/MIS0742-1222310111
 
### Lead user
 
<span class="label contributor">contributor</span>
 
### Hero
 
<span class="label contributor">contributor</span>
 
## Demographics

<span class="label contributor">contributor</span>

In the context of idea communtities, the contributors' demographics such as age, nationality and gender can influence the likelihood of idea selection. Due to prejudices, the contributors' gender can bias the evaluation of their contributions. Besides this, based on the type and purpose of the community, the maturity levels (age groups) of the community members are differently suited and favored. Furthermore, individuals from different origins can bring different prerequisites impacting their ability to engage in innovation processes [1][2].

[1] Beretta, M. (2019). Idea selection in web‐enabled ideation systems. Journal of Product Innovation Management, 36(1), 5-23.

[2] Jensen, M. B., Hienerth, C., & Lettl, C. (2014). Forecasting the commercial attractiveness of user‐generated designs using online data: An empirical study within the LEGO user community. Journal of Product Innovation Management, 31, 75-93.
 
## Idea popularity

Idea popularity marks a high assessment of ideas' value and quality by community members reducing uncertainties and positively impacting their future adaption. In alliance with the assumption that users best know their needs, idea popularity increases the likelihood of idea realization [1][2][3][4]. 

[1] Hoornaert, S., Ballings, M., Malthouse, E. C., & Van den Poel, D. (2017). Identifying new product ideas: waiting for the wisdom of the crowd or screening ideas in real time. Journal of Product Innovation Management, 34(5), 580-597.

[2] Li, M., Kankanhalli, A., & Kim, S. H. (2016). Which ideas are more likely to be implemented in online user innovation communities? An empirical analysis. Decision Support Systems, 84, 28-40.

[3] Ma, J., Lu, Y., & Gupta, S. (2019). User innovation evaluation: Empirical evidence from an online game community. Decision Support Systems, 117, 113-123.

[4] Beretta, M. (2019). Idea selection in web‐enabled ideation systems. Journal of Product Innovation Management, 36(1), 5-23.

## Diversity of collaborators

#### Concept
The diversity of collaborators refers to the composition of teams in collaboration efforts concerning the distribution of knowledge, status, roles, and backgrounds [1][2][3]. Users with more functional diversity view ideas from different angles promoting more creativity in problem-solving [4]. Geographic diversity can impact innovativeness ambiguously. Sharing globally distributed and contextual expertise as well as diverse cultural comprehension can foster innovation activities. However, too diverse views and inputs can lead to unfocused ideas. Nonetheless, shared experiences, norms, and beliefs are important to facilitate mutual understanding [5].

#### Metrics
A popular metric for the aggregation of individual characteristics at different levels while maintaining the associated diversity is the Blau index [6].

[1] Ortu, M., Destefanis, G., Counsell, S., Swift, S., Tonelli, R., & Marchesi, M. (2017). How diverse is your team? Investigating gender and nationality diversity in GitHub teams. Journal of Software Engineering Research and Development, 5(1), 1-18.

[2] Beretta, M. (2019). Idea selection in web‐enabled ideation systems. Journal of Product Innovation Management, 36(1), 5-23.

[3] Fuger, S., Schimpf, R., Füller, J., & Hutter, K. (2017). User roles and team structures in a crowdsourcing community for international development–a social network perspective. Information Technology for Development, 23(3), 438-462.

[4] Shin, S. J., Kim, T. Y., Lee, J. Y., & Bian, L. (2012). Cognitive team diversity and individual team member creativity: A cross-level interaction. Academy of management journal, 55(1), 197-212.

[5] McDonough III, E. F., Kahnb, K. B., & Barczaka, G. (2001). An investigation of the use of global, virtual, and colocated new product development teams. Journal of Product Innovation Management: An international publication of the product development & management association, 18(2), 110-120. 

[6] Blau, P. M. (1977). A macrosociological theory of social structure. American journal of sociology, 83(1), 26-54.
 
## Sentiment
 
 <span class="label contribution">contribution</span> <span class="label initial-contribution">initial contribution</span> <span class="label thread">thread</span> 
 TO DO: <span class="label feedback">feedback</span>
 
#### Concept
 
Sentiment refers to the strength, nature and diversity of affective expressions in discussion elements. Sentiment was found to have a mediating role in the attitudinal and behavioral reaction towards innovative events [1][2]. While positively framed community feedback can have a motivating and activating effect, negative feedback can demotivate [3][4]. However, the expression of a negative sentiment in the presentation of ideas can signal the urgence to intervene in unsatisfactory circumstances and can activate collaborative behavior [5].

#### Metrics

The strength, nature and diversity of sentiments expressed in the formulation of contributions can be measured by the subjectivity and polarity (positivity vs. negativity) [6][7] of the words in a thread's discussion elements (idea, feedback, interaction), and their standard deviation [8], using lexical resources [9]. 

[1] Choi, J. N., Sung, S. Y., Lee, K., & Cho, D. S. (2011). Balancing cognition and emotion: Innovation implementation as a function of cognitive appraisal and emotional reactions toward innovation. Journal of Organizational Behavior, 32(1), 107-124. 

[2] Weiss, H. M., & Cropanzano, R. (1996). Affective events theory. Research in organizational behavior, 18(1), 1-74. 

[3] Reitzig, M., & Sorenson, O. (2013). Biases in the selection stage of bottom‐up strategy formulation. Strategic Management Journal, 34(7), 782-799.

[4] Tsai, H. T., & Bagozzi, R. P. (2014). Contribution behavior in virtual communities: Cognitive, emotional, and social influences. Mis Quarterly, 38(1), 143-164.

[5] Anderson, N. H. (1971). Integration theory and attitude change. Psychological review, 78(3), 171. 

[6] Beretta, M. (2019). Idea selection in web‐enabled ideation systems. Journal of Product Innovation Management, 36(1), 5-23.

[7] Piezunka, H., & Dahlander, L. (2015). Distant search, narrow attention: How crowding alters or-ganizations’ filtering of suggestions in crowdsourcing. Academy of Management Journal, 58(3), 856-880.

[8] Lee, H., & Suh, Y. (2016). Who creates value in a user innovation community? A case study of MyStarbucksIdea. com. Online Information Review.

[9] Baccianella, S., Esuli, A., & Sebastiani, F. (2010, May). Sentiwordnet 3.0: An enhanced lexical resource for sentiment analysis and opinion mining. In Proceedings of the Seventh Interna-tional Conference on Language Resources and Evaluation (LREC'10).

### Subjective Sentiment
 
#### Polarity of words (Textblob, Sentiwordnet)
 
- [``avg_textblob_pol``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_textblob_pol``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``avg_SWN_Polarity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_SWN_Polarity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``idea_textblob_pol``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``idea_SWN_Polarity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``avg_feedback_textblob_pol``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_feedback_textblob_pol``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_feedback_SWN_Polarity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
 
#### Subjectivity of words (Textblob, Sentiwordnet)
 
- [``avg_textblob_sub``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_textblob_sub``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``avg_SWN_Subjectivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_SWN_Subjectivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``idea_textblob_sub``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``avg_feedback_SWN_Subjectivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``avg_feedback_textblob_sub``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_feedback_textblob_sub``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_feedback_SWN_Subjectivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
 
### Positive Sentiment
 
#### Proportion of positive words
 
- [``idea_pos_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``avg_feedback_pos_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_feedback_pos_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``avg_pos_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_pos_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
 
#### Mean positivity of words
 
- [``idea_mean_positivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``avg_feedback_mean_positivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``aggregated_feedback_mean_positivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``avg_mean_positivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``aggregated_mean_positivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
 
### Negative Sentiment
 
#### Proportion of negative words
- [``idea_neg_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``avg_feedback_neg_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``aggregated_feedback_neg_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``avg_neg_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``aggregated_neg_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Mean negativity of words
 
- [``idea_mean_negativity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``avg_feedback_mean_negativity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``aggregated_feedback_mean_negativity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``avg_mean_negativity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``aggregated_mean_negativity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
### Diverse Sentiment
 
#### Standard Deviation of Polarity of words (Textblob, Sentiwordnet)
 
- [``std_textblob_pol``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``std_SWN_Polarity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Standard Deviation of Subjectivity of words (Textblob, Sentiwordnet)
 
- [``std_textblob_sub``](../reference/pici/metrics/basic/#pici.metrics.basic.XY)
- [``std_SWN_Subjectivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Standard Deviation of Mean positivity of words
 
- [``std_mean_positivity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Standard Deviation of Mean negativity of words
 
- [``std_mean_negativity``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
## Elaboration
 
 <span class="label contribution">contribution</span> <span class="label thread">thread</span> 
 
#### Concept
 
Elaboration refers to the degree of quality, readability, and complexity of contributions, and is characterized by two main aspects: text quantity and linguistic style. Novel creations were found to be the product of pre-inventive idea generation and exploration [1][2]. If pre-inventive ideas are original (distinct) and appropriate (relevant, elaborated), the exploration of novel and desired idea attributes can lead to the generation of creative output. Linguistic styles were found to influence writing quality and content comprehension [3]. Writing quality is characterized by lexical sophistication and contains fewer errors [4]. It was found that more successful writers produce longer texts [5]. A more pronounced elaboration indicates that the author is a more knowledgeable and trustworthy expert on the topic [4]. Accordingly, well-elaborated contributions that present a relevant amount of information in a concise and readable manner are more likely to be evaluated, implemented, and reproduced, and thus have a higher innovation potential. 

#### Metrics

Possible elaboration measures are obtained through descriptive statistics techniques [6][7] as well as lexical resource techniques extracting readability and complexity scores [8][9]. 

[1] Finke, R. A., Ward, T. B., & Smith, S. M. (1996). Creative cognition: Theory, research, and applications. MIT press.

[2] Finke, R. A., & Slayton, K. (1988). Explorations of creative visual synthesis in mental image-ry. Memory & cognition, 16(3), 252-257.

[3] Ouyang, J. R., & Stanley, N. (2014). Theories and research in educational technology and dis-tance learning instruction through Blackboard. Universal Journal of Educational Re-search, 2(2), 161-172.

[4] Crossley, S. A., Kyle, K., & McNamara, D. S. (2016). The development and use of cohesive devices in L2 writing and their relations to judgments of essay quality. Journal of Second Language Writing, 32, 1-16.

[5] Crossley, S. A., Roscoe, R., & McNamara, D. S. (2011, June). Predicting human scores of essay quality using computational indices of linguistic and textual features. In International conference on artificial intelligence in education (pp. 438-440). Springer, Berlin, Heidelberg.

[6] Lee, H., Choi, K., Yoo, D., Suh, Y., Lee, S., & He, G. (2018). Recommending valuable ideas in an open innovation community: a text mining approach to information overload problem. Industrial Management & Data Systems.

[7] Li, M., Kankanhalli, A., & Kim, S. H. (2016). Which ideas are more likely to be implemented in online user innovation communities? An empirical analysis. Decision Support Systems, 84, 28-40.

[8] Agichtein, E., Castillo, C., Donato, D., Gionis, A., & Mishne, G. (2008, February). Finding high-quality content in social media. In Proceedings of the 2008 international conference on web search and data mining (pp. 183-194).

[9] Rhyn, M., & Blohm, I. (2017). A machine learning approach for classifying textual data in crowdsourcing.
 
### High Elaboration
 
#### Length of text (number of words)

- [``avg_thread_length``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
- [``aggregated_thread_length``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Number of syllables

- [``avg_number_syllables_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
- [``aggregated_number_syllables_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Punctuation Density (Proportion of all characters)

- [``avg_content_punctuation_prop_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
- [``aggregated_content_punctuation_prop_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Spacing Density (proportion of all characters)
 
#### Capitalization Density (proportion of all characters)
 
#### Flesch-Reading-Ease Score

- [``flesch_reading_ease``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Automatic Readability Index

- [``automated_readability_index``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
### Complex Elaboration
 
#### Number of References (links)

- [``avg_neg_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
- [``aggregated_neg_prop``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Flesch-Kincaid Formula

- [``flesch_kincaid_grade``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Smog Grading

- [``smog_index``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Coleman-Lieau Index

- [``coleman_liau_index``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Dale-Chall Readbility Score

- [``dale_chall_readability_score``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Number of difficult words

- [``difficult_words``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
#### Linsear Write Formula

- [``linsear_write_formula``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
### Low Elaboration
 
#### Number of Spelling Mistakes

- [``avg_spelling_mistakes_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``aggregated_spelling_mistakes_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO  
 
#### Number of Punctuation Mistakes

- [``avg_content_punctuations_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
- [``aggregated_content_punctuations_thread``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 
 
## Distinctiveness
 
 <span class="label contribution">contribution</span> <span class="label thread">thread</span> 
 
#### Concept
 
Distinctiveness refers to the contributions' uniqueness and novelty by capturing the degree of similarity of a contribution to the other ones in a community. Distinct contributions discuss content that substantially differs from other ideas, and contains distant knowledge and novelty [1]. Novelty and abstraction in problem formulation can foster creativity in the subsequent solution processing [2]. Promising ideas have an optimal level of creativity, balance novelty with familiarity, and are associated with rarity and high user demand [3].

#### Metrics

Distinctiveness can be measured with the aid of descriptive statistics techniques [5][6] and topic distribution techniques [7].

[1] Piezunka, H., & Dahlander, L. (2015). Distant search, narrow attention: How crowding alters or-ganizations’ filtering of suggestions in crowdsourcing. Academy of Management Journal, 58(3), 856-880.

[2] Finke, R. A., Ward, T. B., & Smith, S. M. (1996). Creative cognition: Theory, research, and applications. MIT press.

[3] Resch, K., Fellner, M., Fahrenwald, C., Slepcevic-Zach, P., Knapp, M., & Rameder, P. (2020). Embedding Social Innovation and Service Learning in Higher Education's Third Sector Policy Developments in Austria. In Frontiers in Education (p. 112). Frontiers.

[5] Rhyn, M., & Blohm, I. (2017). A machine learning approach for classifying textual data in crowdsourcing.

[6] Moehrle, M. G., Wustmans, M., & Gerken, J. M. (2018). How business methods accompany technological innovations–a case study using semantic patent analysis and a novel informetric measure. R&D Management, 48(3), 331-342.

[7] Blei, D. M. (2012). Probabilistic topic models. Communications of the ACM, 55(4), 77-84.

### High Distinctiveness
 
#### TF.IDF-indices (Specificity) 
 
- [``tfidf_sum``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO
- [``tfidf_avg``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO  
 
#### Topic Structure with LDA

- probability per topic (total number of topics depends on highest coherence score)

## Community feedback

 <span class="label contribution">contribution</span> <span class="label thread">thread</span> 

#### Concept

Online communities provide their members with the possibility to give feedback by commenting on published contributions. The feedback was found to be one of the main benefits for innovators joining a community as an important determinant of a contribution's innovative advancement [Franke & Shah 2003] [Hoonaert 2017] [Jensen 2014]. The provision of high-quality assistance from innovative collaborators enhances product optimizations and facilitates the diffusion of emerging innovations.

#### Metrics

Community feedback can be measured by its quantity [Hoonaerth] [Martinez-Torres 2016] [Lee 2018] [Chan et al 2020], positivity [Jensen 2014] [Ogink 2019], and quality, e.g. feedback from users with high reputation or experience (top commenter / previously launched ideas).

### Number of comments

### Length of comments

### Feedback length dispersion

### Feedback from top commenters
 
## Activity level

<span class="label community">community</span>

### Concept

The factor "Activity Level" represents the aggregated degree of interaction and engagement at community level. The higher the activity level the more ideas and comments are shared, and the greater the prevalence of innovation activity assuming contribution quality remains constant. Also, highly active communities might attract more active and therefore innovative users whose engagement in turn lifts community activity culminating in self-reinforcing effects. Additionally, the community's age influences its activity level. In its early stages, a peer community draws more attention and sparks curiosity in potential contributors. Thisinterest and engagement tends to decline over time. However, communities can build their user base and optimize structures as they mature, which in turn has a positive impact on activity. 

[1] Bayus, B. L. (2013). Crowdsourcing new product ideas over time: An analysis of the Dell IdeaStorm community. Management science, 59(1), 226-244.

[2] Chan, K. W., Li, S. Y., Ni, J., & Zhu, J. J. (2021). What feedback matters? The role of experience in motivating crowdsourcing innovation. Production and Operations Management, 30(1), 103-126.

[3] Hoornaert, S., Ballings, M., Malthouse, E. C., & Van den Poel, D. (2017). Identifying new product ideas: waiting for the wisdom of the crowd or screening ideas in real time. Journal of Product Innovation Management, 34(5), 580-597.

[4] Li, M., Kankanhalli, A., & Kim, S. H. (2016). Which ideas are more likely to be implemented in online user innovation communities? An empirical analysis. Decision Support Systems, 84, 28-40.

[5] Ma, J., Lu, Y., & Gupta, S. (2019). User innovation evaluation: Empirical evidence from an online game community. Decision Support Systems, 117, 113-123.

[6] Piezunka, H., & Dahlander, L. (2015). Distant search, narrow attention: How crowding alters organizations’ filtering of suggestions in crowdsourcing. Academy of Management Journal, 58(3), 856-880.


#### Same day submissions

- [``Same day submissions``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO

#### Number of month since the inception of the community (community age)

- [``Number of month since the inception of the community``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO

#### Time-varying effects (Month, year of contribution)

- [``Time-varying effects (Month, year of contribution)``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO

## Prominence

<span class="label community">community</span>

#### Concept

The innovation influencing factor "Prominence" describes a community’s level of recognition from outside. The higher the community’s position in online search rankings and the better connected through website link networks, the more awareness it enjoys from users. Popular communities are more likely to have many contributors and thus a higher activity level.

#### Metrics

Possible measures for prominence are the community's position on Twitter [1], website link networks [2], or monthly online search volumes with respect to the community [3]. 

[1] Menichinelli, M., & Schmidt, A. G. S. (2019). First exploratory geographical and social maps of the maker movement. European Journal of Creative Practices in Cities and Landscapes, 2(2), 35-62.

[2] De Filippi, P., & Hassan, S. (2015). Measuring value in commons-based ecosystem: bridging the gap between the commons and the market. The MoneyLab Reader. Institute of Network Cultures, University of Warwick.

[3] Ma, J., Lu, Y., & Gupta, S. (2019). User innovation evaluation: Empirical evidence from an online game community. Decision Support Systems, 117, 113-123.

#### Google search trends

- [``Google search trends``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO

#### Position on Twitter

- [``position on Twitter``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO

#### Website link networks

- [``website link networks``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO

## Crowd vs community
 
### Lorenz curve
 
<span class="label community">community</span>
 
#### Concept
 
The Lorenz curve of % posts (x-axis) made by % contributors (y-axis) can be used to indicate contribution inequality in communities.
 
#### Metrics
 
Community:
- [``% contributors`` + ``% posts``](../reference/pici/metrics/basic/#pici.metrics.basic.lorenz)
 
#### Visualizations
 
- [``plot_lorenz_curves``](../reference/pici/visualizations/#pici.visualizations.plot_lorenz_curves)

## Openness

<span class="label community">community</span>

#### Concept

Openness refers to the accessibility of projects and processes to external parties. A high degree of openness, for example through open project licenses in the open-source software or hardware area, makes it easier for users to participate in and modify projects driving innovation [1]. 

#### Metrics

To measure the degree of openness in open-source hardware projects, [2] developed the "Open-O-Meter," which tests the following criteria: (1) the presence of a version control system with editing capabilities for all, (2) guidance on how to contribute, and (3) the presence of a bug tracking system. The existence of these criteria depends on the technical equipment and organization of the community.

[1] Bonvoisin, J., Mies, R., Boujut, J. F., & Stark, R. (2017). What is the “source” of open source hardware?.

[2] Bonvoisin, J., & Mies, R. (2018). Measuring openness in open source hardware with the open-o-meter. Procedia CIRP, 78, 388-393.

#### Type of license

- [``Type of license``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 

#### Accessibility of files/design/documentation/instructions

- [``Accessibility of files/design/documentation/instructions``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 

#### version control system

- [``version control system``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 

#### guidance on how to contribute

- [``guidance on how to contribute``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 

#### Issue tracking

- [``Issue tracking``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 

#### Use of collaborative tools

- [``Use of collaborative tools``](../reference/pici/metrics/basic/#pici.metrics.basic.XY) # TO DO 

