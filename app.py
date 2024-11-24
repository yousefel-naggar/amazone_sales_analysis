# Importing Libraries
import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv(r"datasets/optimized_amazone_data.csv")
df.drop(columns="Unnamed: 0", inplace=True)

# Set up the Streamlit app layout
st.title("Amazon Sales Analysis")
st.sidebar.header("Navigation")


# Sidebar - Selection
sidebar_option = st.sidebar.radio("Choose an Option:", ["Data Overview", "EDA"])


# Display the data overview
if sidebar_option == "Data Overview":
    st.header("Data Overview")
    st.write("This dataset is having the data of 1K+ Amazon Product's Ratings and Reviews as per their details listed on the official website of Amazon")
    st.write(df.head())
    st.markdown("### Dataset Summary (numerical)")
    st.write(df.describe())
    st.markdown("### Dataset Summary (categorical)")
    st.write(df.describe(include='object'))
    
# 2. EDA part
elif sidebar_option == "EDA":
     st.header("Exploratory Data Analysis")

     
     # 1. Put a select radio to choose to see a uni or bivariant analysis
     analysis_type_option = st.sidebar.radio("Choose type of Analysis:", ["Univariate Analysis", "Bivariate Analysis"])
     if analysis_type_option == "Univariate Analysis":
        st.subheader("Univariate Analysis")
        # 1.1 Plot a histogram of the rating column
        st.markdown("### Rating Distribution")
        fig1, ax = plt.subplots()
        sns.histplot(data=df['rating'], ax=ax)
        st.pyplot(fig1)
        fig2, ax = plt.subplots()
        sns.kdeplot(df['rating'])
        st.pyplot(fig2)
        st.write("Insights:")
        #st.write("* We can note that the distribution of `rating` column is a normal distribution plot.") 
        #st.write("* Average of `rating` it may equal 4.2.")
        st.write("* The distribution is left skewed, with a longer tail towards higher ratings. This indicates that there are more ratings on the higher end of the scale compared to the lower end.")
        st.write("Recommendations:")
        st.write("* Analyze the reviews associated with lower ratings to identify areas where improvements can be made.")
        st.write("* Consider tailoring marketing campaigns to appeal to the specific preferences of users who tend to give higher ratings.")

     elif analysis_type_option == "Bivariate Analysis":
         bivariate_type_option = st.sidebar.radio("Choose Analysis:", ["actual price & discounted price", "rating & category","Quality Level & actual_price"])


         if bivariate_type_option == "actual price & discounted price":
             st.write("Show scatter Plot `actual_price` with `discounted_price`:")
             fig3, ax = plt.subplots()
             sns.regplot(x=df['actual_price'],y=df['discounted_price'],scatter_kws={'color':'blue'}, line_kws={'color':'orange'} , ax=ax)
             st.pyplot(fig3)
             st.write("Insights:")
             st.write("* There is a strong positive correlation between the actual price and the discounted price. This means that as the actual price increases, the discounted price also tends to increase.")
             st.write("Recommendations:")
             st.write("* focus on discounting high value items might yield higher revenue.")
             st.write("* Maintaining a similar discounting strategy across different price ranges could be beneficial.")
             


         elif bivariate_type_option == "rating & category":
            st.write("* show the min `rating` for each `category`")
            fig4 , ax = plt.subplots()
            data = df.groupby('sub_category')['rating'].min()
            sns.barplot(x=data.values,y=data.index,color='green',width=0.2,ax=ax)
            plt.xlabel('Average Rating')
            plt.ylabel('Category')
            plt.xlim([0,5.5])
            st.pyplot(fig4)

            st.write("* show the max `rating` for each `category`")
            fig5 , ax = plt.subplots()
            data = df.groupby('sub_category')['rating'].max()
            sns.barplot(x=data.values,y=data.index,color='green',width=0.2,ax=ax)
            plt.xlabel('Average Rating')
            plt.ylabel('Category')
            plt.xlim([0,5.5])
            st.pyplot(fig5)

            st.write("* show the average `rating` for each `category`")
            fig6 , ax = plt.subplots()
            data = df.groupby('sub_category')['rating'].mean()
            sns.barplot(x=data.values,y=data.index,color='green',width=0.2,ax=ax)
            plt.xlabel('Average Rating')
            plt.ylabel('Category')
            plt.xlim([0,5.5])
            st.pyplot(fig6)

            st.write("Insights:")
            st.write("* Categories such as `Electronics`, `Health & Personal Care`, and `Home & Kitchen` have moderate average ratings. These ratings suggest that while these categories may generally meet customer expectations, there could be room for improvement in product quality or customer service to increase satisfaction.")
            st.write("* `Car & Motorbike` and `Computers & Accessories` categories have relatively high average ratings, indicating that customers are generally satisfied with products in these categories. This could imply that these categories offer high-quality products or have effective quality control measures in place. ")
            
            st.write("Recommendations:")
            st.write("* We can handle categories that have high rating by doing effective marketing.")
            st.write("* we can improve products that have low rating categories by Focus on Customer Feedback in \nLower-Rated Categories .")
            st.write("* Analyzing customer reviews in categories like `Home Improvement` and `Office Products` may reveal common complaints or areas that need enhancement")



         elif bivariate_type_option == "Quality Level & actual_price":
             st.write("* Show `Quality Level` for each `actual_price`")
             fig7 = sns.catplot(x=df['Quality Level'],y=df['actual_price'],width=0.2)
             plt.xlabel('Quality Level')
             plt.ylabel('actual_price')
             plt.xticks(rotation=45)
             st.pyplot(fig7)

             #fig8 = sns.catplot(x=df['Quality Level'],y=df['sub_category'])
             #plt.xlabel('Quality Level')
             #plt.ylabel('actual_price')
             #plt.xticks(rotation=45)
             #plt.yticks(rotation=45)
             #plt.figure(figsize=(4, 2))
             #st.pyplot(fig8)

             st.write("* Distribution of mean of Products price by Quality Level")
             data = df.groupby(['Quality Level'])['actual_price'].mean()
             fig9 = px.pie(data, 
                values=data.values, 
                names=data.index)
             fig9.update_layout(width=500, height=500) 
             st.plotly_chart(fig9)

             st.write("* Distribution of count of Products by Quality Level")
             data = df.groupby(['Quality Level'])['product_id'].count()
             fig10 = px.pie(data, 
                         values=data.values, 
                         names=data.index )
             fig10.update_layout(width=500, height=500) 
             st.plotly_chart(fig10)

             st.write("Insights:")
             st.write("* not that products classified as `below average`, `exceptional`, and `poor` account for less than '5%' of the total. This could indicate that the store does not carry many lower-quality items, or that demand for them is low.")

             st.write("Recommendations:")
             st.write("* `poor` and `below average` have large mean price percent for the quality level  \n\t* we can improve products that have low quality level ")
             st.write("* Increasing Variety in 'Good' or 'Below Average' Products could help attract a broader range of customers with different budgets. ")
             st.write("* Analyzing 'Poor' Products to understand why they are rated poorly and exploring options for quality improvement or sourcing adjustments if these products are in demand but currently low-quality.")
             st.write("* Promoting 'Exceptional' Products as unique, premium options could help attract customers looking for highly distinctive, top-quality items.")

             
 
