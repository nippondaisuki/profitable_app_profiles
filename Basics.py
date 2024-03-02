#!/usr/bin/env python
# coding: utf-8

# # Profitable App Profiles for the App Store and Google Play Markets
# 
# The objective of our project is to identify mobile application profiles that demonstrate profitability within the App Store and Google Play markets. As data analysts employed by a company specializing in Android and iOS app development, our role is to equip our team of developers with data-driven insights to guide their app creation decisions.
# 
# Within our company, we exclusively produce free-to-download and install apps, relying primarily on in-app advertisements for revenue generation. Consequently, the success of our apps is heavily reliant on user engagement. Our primary aim in this project is to conduct data analysis to provide our developers with insights into the types of apps likely to garner greater user interest.

# ## Opening and Exploring the Data
# 
# As of September 2018, the App Store hosted around 2 million iOS apps, while Google Play boasted 2.1 million Android apps.
# 
# ![img](https://s3.amazonaws.com/dq-content/350/py1m8_statista.png) Source: [Statista](https://www.statista.com/statistics/276623/number-of-apps-available-in-leading-app-stores/)
# 
# Gathering data for over four million apps demands considerable time and financial resources. Hence, our approach will involve analyzing a representative sample of data instead. To circumvent the need for extensive data collection efforts, we aim to explore existing datasets that align with our research objectives. Fortunately, two datasets appear suitable:
# 
# + A [dataset](https://www.kaggle.com/lava18/google-play-store-apps) encompassing data for roughly ten thousand Android apps from Google Play, available for download via this [link](https://dq-content.s3.amazonaws.com/350/googleplaystore.csv).
# + A [dataset](https://www.kaggle.com/ramamet4/app-store-apple-data-set-10k-apps) containing information on approximately seven thousand iOS apps from the App Store, accessible through this [link](https://dq-content.s3.amazonaws.com/350/AppleStore.csv).
# 
# Let's initiate our analysis by accessing these datasets and delving into their contents.

# In[1]:


from csv import reader

### The Google Play data set ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store data set ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# In order to facilitate the exploration of the two datasets, we will initially develop a function called `explore_data()`. This function will enable us to navigate through rows in a clearer format, and we'll incorporate an option within the function to display the count of rows and columns for any given dataset.

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line after each row

    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))
        
print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# We can now see that the Google Play data set has 10,841 rows and 13 columns. We have identified the 'App', 'Category', 'Reviews', 'Installs', 'Type', 'Price', and 'Genre' columns that could help us with our analysis.
# 
# Now, let's explore the App Store data set.

# In[3]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# We have 7,197 iOS apps in this data set. The columns which are of interest to us are the 'id', 'currency', 'price', 'rating_count_tot', 'rating_count_ver', and 'prime_genre'. The columns may not be self-explanatory, so here is the [link](https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps) to the data set documentation for reference.

# ## Deleting Wrong Data
# The Google Play data set has a [dedicated discussion section](https://www.kaggle.com/datasets/lava18/google-play-store-apps/discussion), and we can see that [one of the discussions](https://www.kaggle.com/datasets/lava18/google-play-store-apps/discussion/66015) describes an error for row 10,472. Let's print this row, along with the header row and another row that is correct for comparison.
# 

# In[4]:


print(android[10472]) #incorrect row
print('\n')
print(android_header) #header
print('\n')
print(android[0]) #correct row


# The row 10,472 corresponds to the app 'Life Made WI-Fi Touchscreen Photo Frame', and its rating is 19, which is not possible as the maximum rating is supposed to be 5. This issue shows that there is a missing value in the 'Category' column. Therefore, we'll delete this row.

# In[5]:


print(len(android))
del android[10472] # don't run this more than once
print(len(android))


# # Removing Duplicate Entries
# ## Part One
# Upon exploring the Google Play data set, we'll discover that there are multiple duplicate entries. For example, Instagram has four entries:

# In[6]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# In total, there are 1,181 cases of duplicate entries:

# In[7]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
        
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# Before analyzing the data, we should remove any duplicate entries so as to avoid counting any apps more than once. One way to do this is by removing the duplicate rows randomly, but there is a better way.
# 
# If you examine the rows that we printed two cells above for the Instagram app, the main difference happens on the fourth position of each row, which corresponds to the number of reviews. The different numbers show the data was collected at different times. We can use this to build a criterion for removing the duplicates. Instead of removing duplicates randomly, we'll only keep the row with the highest number of reviews as this means that the data is the most recent, hence, is more reliable than others. As for the latter, we'll remove them.
# 
# To do that, we will:
# 
# + Create a dictionary where each key is a unique app name, and the value is the highest number of reviews of that app
# + Use the dictionary to create a new data set, which will have only one entry per app (and we only select the apps with the highest number of reviews)

# # Part Two
# ## Let's begin by creating a dictionary

# In[8]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews
    


# In the previous code cell, we have found 1,181 cases of duplicate entries. Hence, we should expect that the length of our dictionary be equal to the difference between the length of the data set and 1,181.

# In[9]:


print('Expected length:', len(android) - 1181)
print('Actual length:', len(reviews_max))


# Now, let's use the `reviews_max` dictionary to remove the duplicate rows. In the code cell below:
# 
# + We will start by creating two empty lists, `android_clean` and `already_added`.
# + We loop through the Google Play dataset, and for each iteration, do the following: 
#     + Isolate the name of the app and the number of reviews
#     + Append the entire row to the `android_clean` list (which will eventually be a list of lists and store our cleaned data set), and
#     + Append the name of the app name to the `already_added` list - this helps us to keep track of apps that we already added, if:
#         + `n_reviews` is the same as the number of maximum reviews of the app name, and
#         + name is not already in the list `already_added`. We need to add this supplementary condition to account for those cases where the highest number of reviews of a duplicate app is the same for more than one entry (for example, the Box app has three entries, and the number of reviews is the same). If we just check for `reviews_max[name] == n_reviews`, we'll still end up with duplicate entries for some apps.

# In[10]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name) # make sure this is inside the if block


# Now, let's quickly explore the data set, and confirm that it has 9,659 rows.

# In[11]:


explore_data(android_clean, 0, 3, True)


# We now have 9,659 rows, just as expected.

# # Removing Non-English Apps
# ## Part One
# If we explore the data long enough, we'll find that both data sets have apps with names that suggest they are not designed for an English-speaking audience. Below, we can see a couple of examples from both data sets:

# In[12]:


print(ios[813][1])
print(ios[6731][1])
print('\n')
print(android_clean[4412][0])
print(android_clean[7940][0])


# We're not interested in keeping these apps, so we'll remove them. One way to do this is to remove each app with a name containing a symbol that isn't commonly used in English text - English text usually includes letters from the English alphabet, numbers composed of digits from 0 to 9, punctuation marks and other symbols.
# 
# Each character we use in a string has a corresponding number associated wit it. We can get the corresponding number of each character using the `ord()` built-in function.

# In[13]:


def is_english(string):
    
    for character in string:
        if ord(character) > 127:
            return False
        
    return True

print(is_english('Instagram'))
print(is_english('爱奇艺PPS -《欢乐颂2》电视剧热播'))
    


# The function seems to work fine, but some English apps use emojis or other symbols which are not included in the ASCII range. Hence, we'll remove useful English apps if we use the function at its current form.

# In[14]:


print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))

print(ord('™'))
print(ord('😜'))


# # Part Two
# To minimize the impact of data loss, we'll only remove an app if its name has more than three characters with corresponding numbers falling outside the ASCII range.

# In[15]:


def is_english(string):
    
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
            
    if non_ascii > 3:
        return False
    
    else:    
        return True

print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# Our filter function is still not perfect, but it should be fairly effective.
# Below, we use the updated `is_english()` function to filter out the non-English apps for both data sets:

# In[16]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# We can see that we now have 9,614 Android apps and 6,183 iOS apps.

# # Isolating The Free Apps
# As mentioned in the introduction, we only build apps that are free to download and install, and our main source of revenue consists of in-app ads. Our datasets contain both free and non-free apps; we'll need to isolate only the free apps for our analysis.

# In[17]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))
    


# We're left with 8864 Android apps and 3222 iOS apps, which should be enough for our analysis.

# # Most Common Apps by Genre
# ## Part One
# As we mentioned in the introduction, our aim is to determine the kinds of apps that are likely to attract more users because our revenue is highly influenced by the number of people using our apps.
# 
# To minimize risks and overhead, our validation strategy for an app idea is comprised of three steps:
# 
# 1. Build a minimal Android version of the app, and add it to Google Play.
# 2. If the app has a good response from users, we develop it further.
# 3. If the app is profitable after six months, we build an iOS version of the app and add it to the App Store.
# 
# Because our end goal is to add the app on both Google Play and the App Store, we need to find app profiles that are successful on both markets. For instance, a profile that works well for both markets might be a productivity app that makes use of gamification.
# 
# Let's begin the analysis by getting a sense of what are the most common genres for each market. For this, we'll need to build frequency tables for the `prime_genre` column of the App Store data set, and the `Genres` and `Category` columns of the Google Play data set.
# 

# # Part Two
# We'll build two functions we can use to analyze the frequency tables:
# + One function to generate frequency tables that show percentages
# + Another function we can use to display the percentages in a descending order

# In[18]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])
    


# # Part Three
# We start by analyzing the frequency table for the `prime_genre` column of the App Store data set.

# In[19]:


display_table(ios_final, -5)


# We can clearly see that the most common genre among the free English apps is Games, at 58.2%. Entertainment comes next at 7.9%, followed by Photo & Video at 5.0%, Education at 3.7%, and Social Networking at 3.3%.
# 
# The general impression is that most of the apps in the App Store are designed for entertainment, rather than for practical purposes. However, this does not mean that there are more users in the former as compared to the latter. There could be a supply-demand imbalance.
# 
# Let's continue by examining the `Genres` and `Category` columns of the Google Play data set (two columns which seem to be related).

# In[20]:


display_table(android_final, 1) # Category


# Looking at the results in the cell above, we can see that there are more apps in the Google Play data set which are centred around practical purposes such as family, tools, business, lifestyle and productivity. This is the opposite of the situation for the App Store. However, upon doing a quick research on Google Play, we can see that games for kids mostly make up the majority of the family category. 
# 
# Even so, practical apps seem to have a better representation on Google Play compared to App Store. This picture is also confirmed by the frequency table we see for the Genres column:

# In[21]:


display_table(android_final, -4)


# The difference between the Genres and the Category columns is not crystal clear, but one thing we can notice is that the Genres column is much more granular (it has more categories). We're only looking for the bigger picture at the moment, so we'll only work with the Category column moving forward.
# 
# Up to this point, we found that the App Store is dominated by apps designed for fun, while Google Play shows a more balanced landscape of both practical and for-fun apps. Now we'd like to get an idea about the kind of apps that have most users.

# # Most Popular Apps by Genre on the App Store
# One way to find out what genres are the most popular (have the most users) is to calculate the average number of installs for each app genre. For the Google Play dataset, we can find this information in the Installs column, but this information is missing for the App Store dataset. As a workaround, we'll take the total number of user ratings as a proxy, which we can find in the rating_count_tot app.
# 
# Let's start with calculating the average number of user ratings per app genre on the App Store.

# In[22]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# On average, navigation apps have the highest number of user reviews, but this figure is heavily influenced by Waze and Google Maps, which have close to half a million user reviews together:

# In[23]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) # print name and number of ratings


# The same pattern applies to social networking apps, where the average number is heavily influenced by a few giants like Facebook, Pinterest, Skype, etc. Same applies to music apps, where a few big players like Pandora, Spotify, and Shazam heavily influence the average number.
# 
# Our aim is to find popular genres, but navigation, social networking or music apps might seem more popular than they really are. The average number of ratings seem to be skewed by very few apps which have hundreds of thousands of user ratings, while the other apps may struggle to get past the 10,000 threshold. We could get a better picture by removing these extremely popular apps for each genre and then rework the averages, but we'll leave this level of detail for later.
# 
# Reference apps have 74,942 user ratings on average, but it's actually the Bible and Dictionary.com which skew up the average rating:

# In[24]:


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# However, this niche seems to show some potential. One thing we could do is take another popular book and turn it into an app where we could add different features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes about the book, etc. On top of that, we could also embed a dictionary within the app, so users don't need to exit our app to look up words in an external app.
# 
# This idea seems to fit well with the fact that the App Store is dominated by for-fun apps. This suggests the market might be a bit saturated with for-fun apps, which means a practical app might have more of a chance to stand out among the huge number of apps on the App Store.
# 
# Other genres that seem popular include weather, book, food and drink, or finance. The book genre seem to overlap a bit with the app idea we described above, but the other genres don't seem too interesting to us:
# 
# Weather apps — people generally don't spend too much time in-app, and the chances of making profit from in-app adds are low. Also, getting reliable live weather data may require us to connect our apps to non-free APIs.
# 
# Food and drink — examples here include Starbucks, Dunkin' Donuts, McDonald's, etc. So making a popular food and drink app requires actual cooking and a delivery service, which is outside the scope of our company.
# 
# Finance apps — these apps involve banking, paying bills, money transfer, etc. Building a finance app requires domain knowledge, and we don't want to hire a finance expert just to build an app.
# 
# Now let's analyze the Google Play market a bit.

# # Most Popular Apps by Genre on Google Play
# We have data about the number of installs for the Google Play market, so we should be able to get a clearer picture about genre popularity. However, the install numbers don't seem precise enough — we can see that most values are open-ended (100+, 1,000+, 5,000+, etc.):

# In[25]:


display_table(android_final, 5) # the Installs columns


# For instance, we don't know whether an app with 100,000+ installs has 100,000 installs, 200,000, or 350,000. However, we don't need very precise data for our purposes — we only want to find out which app genres attract the most users.
# 
# We're going to leave the numbers as they are, which means that we'll consider that an app with 100,000+ installs has 100,000 installs, and an app with 1,000,000+ installs has 1,000,000 installs, and so on. To perform computations, however, we'll need to convert each install number from a string to a float. This means we need to remove the commas and the plus characters, or the conversion will fail and cause an error. We'll do this directly in the loop below, where we also compute the average number of installs for each genre (category).

# In[26]:


categories_android = freq_table(android_final, 1)

for category in categories_android:
    total = 0
    len_category = 0
    for app in android_final:
        category_app = app[1]
        if category_app == category:
            n_installs = app[5]
            n_installs = n_installs.replace(',', '')
            n_installs = n_installs.replace('+', '')
            total += float(n_installs)
            len_category += 1
    avg_n_installs = total / len_category
    print(category, ':', avg_n_installs)


# On average, communication apps have the most installs: 38,456,119. This number is heavily skewed up by a few apps that have over one billion installs (WhatsApp, Facebook Messenger, Skype, Google Chrome, Gmail, and Hangouts), and a few others with over 100 and 500 million installs:

# In[27]:


for app in android_final:
    if app[1] == 'COMMUNICATION' and (app[5] == '1,000,000,000+'
                                     or app[5] == '500,000,000+'
                                     or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# If we removed all the communication apps that have over 100 million installs, the average would be reduced roughly ten times:

# In[28]:


under_100_m = []

for app in android_final:
    n_installs = app[5]
    n_installs = n_installs.replace(',', '')
    n_installs = n_installs.replace('+', '')
    if (app[1] == 'COMMUNICATION') and (float(n_installs) < 100000000):
        under_100_m.append(float(n_installs))
        
sum(under_100_m) / len(under_100_m)


# We see the same pattern for the video players category, which is the runner-up with 24,727,872 installs. The market is dominated by apps like Youtube, Google Play Movies & TV, or MX Player. The pattern is repeated for social apps (where we have giants like Facebook, Instagram, Google+, etc.), photography apps (Google Photos and other popular photo editors), or productivity apps (Microsoft Word, Dropbox, Google Calendar, Evernote, etc.).
# 
# Again, the main concern is that these app genres might seem more popular than they really are. Moreover, these niches seem to be dominated by a few giants who are hard to compete against.
# 
# The game genre seems pretty popular, but previously we found out this part of the market seems a bit saturated, so we'd like to come up with a different app recommendation if possible.
# 
# The books and reference genre looks fairly popular as well, with an average number of installs of 8,767,811. It's interesting to explore this in more depth, since we found this genre has some potential to work well on the App Store, and our aim is to recommend an app genre that shows potential for being profitable on both the App Store and Google Play.
# 
# Let's take a look at some of the apps from this genre and their number of installs:

# In[29]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE':
        print(app[0], ':', app[5])


# The book and reference genre includes a variety of apps: software for processing and reading ebooks, various collections of libraries, dictionaries, tutorials on programming or languages, etc. It seems there's still a small number of extremely popular apps that skew the average:

# In[30]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000,000+'
                                            or app[5] == '500,000,000+'
                                            or app[5] == '100,000,000+'):
        print(app[0], ':', app[5])


# However, it looks like there are only a few very popular apps, so this market still shows potential. Let's try to get some app ideas based on the kind of apps that are somewhere in the middle in terms of popularity (between 1,000,000 and 100,000,000 downloads):

# In[31]:


for app in android_final:
    if app[1] == 'BOOKS_AND_REFERENCE' and (app[5] == '1,000,000+'
                                            or app[5] == '5,000,000+'
                                            or app[5] == '10,000,000+'
                                            or app[5] == '50,000,000+'):
        print(app[0], ':', app[5])


# In[ ]:


This niche seems to be dominated by software for processing and reading ebooks, as well as various collections of libraries and dictionaries, so it's probably not a good idea to build similar apps since there'll be some significant competition.

We also notice there are quite a few apps built around the book Quran, which suggests that building an app around a popular book can be profitable. It seems that taking a popular book (perhaps a more recent book) and turning it into an app could be profitable for both the Google Play and the App Store markets.

However, it looks like the market is already full of libraries, so we need to add some special features besides the raw version of the book. This might include daily quotes from the book, an audio version of the book, quizzes on the book, a forum where people can discuss the book, etc.

