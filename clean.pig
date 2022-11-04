file1 = LOAD '/user/vagrant/final_data.csv' using PigStorage('|') AS (reviewerId:chararray,text:chararray, label:chararray);

-- Clean - Keep only label 0 and 1
A = FILTER file1 BY label == '0' OR label == '1';

-- Clean - Convert to lower case
B = foreach A  generate reviewerId,LOWER(text) as text,label;



--Clean - Keep only words
C = foreach B  generate reviewerId,REPLACE(text,'([^a-zA-Z\\s]+)','') as text,label;

D = foreach C  generate reviewerId, text,REPLACE(label,'0','ham') as label;

E = foreach D  generate reviewerId, text,REPLACE(label,'1','spam') as label;
store E into '/user/vagrant/csvoutput' using PigStorage('|','-schema');
-- HAM = FILTER E BY label == 'ham';
-- SPAM = FILTER E BY label == 'spam';


-- HAM_GROUP = GROUP HAM BY(reviewerId)
-- counted = FOREACH HAM GENERATE reviewerId, COUNT(label) as cnt;
-- result = LIMIT counted 5;
-- dump result;