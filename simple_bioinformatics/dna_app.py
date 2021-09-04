import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image

# Image and Header
image = Image.open('dna-logo.jpg')

st.image(image, use_column_width=True)

st.write("""
# DNA Nucleotide Count Web App

This app counts the nucleotide composition of query DNA!

***
""")

# Text Box for the DNA sequence
st.header('Enter DNA Sequence')
st.write("""
*Note: The first line is skipped because it is assumed the first line is the name of the sequence*
""")

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

sequence = st.text_area('Sequence input', sequence_input, height=250)
sequence = sequence.splitlines()
sequence = sequence[1:] # Skip the first line/Sequence name
sequence = ''.join(sequence)

st.write("""
***
""")

# Print input DNA sequence
st.header('INPUT (DNA Query)')
sequence

# DBA nucleotide count
st.header('OUTPUT (DNA Nucleotide Count)')

# 1. Dict
st.subheader('1. Print dictionary')
def dna_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C'))
    ])
    return d

dna_dict = dna_nucleotide_count(sequence)
dna_dict

# 2. Print text
st.subheader('2. Print text')
st.markdown("""
There are {A} adenine (A).

There are {T} thymine (T).

There are {G} guanine (G).

There are {C} cytosine (C).
""".format(**dna_dict))

# 3. Display dataframe
st.subheader('3. Display dataframe')
df = pd.DataFrame.from_dict(dna_dict, orient='index') # Create df
df = df.rename({0: 'count'}, axis='columns') # Rename column of nucleotide counts
df.reset_index(inplace=True) # Move nucleotide from index to column
df = df.rename(columns={'index': 'nucleotide'}) # Rename nucleotide column
st.write(df) # Write DF to page

# 4. Bar chart using Altair
st.subheader('4. Display bar chart')
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(80)
)
st.write(p)