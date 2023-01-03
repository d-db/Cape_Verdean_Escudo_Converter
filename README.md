# Cape Verdean Escudo - Euro Converter

## Project Summary

Learning #Python and tired of counting your Cape Verdean #Escudos? Then you might be interested in this little project. 

It is my interpretation of the capstone exercise of [Giles McMullen Python-course on Udemy](https://www.udemy.com/course/the-complete-python-programmer-bootcamp/). The final function takes as arguments the path to a picture of your Escudo-Coins and the current exchange rate EUR – CVE and returns, thanks to image analysis, the amount of the photographed coins in Escudos and Euro.

I decided to program the classification of the coins relative to the size of a 50 Escudos coin, so that photos from different distances could be analyzed (like in the video). Hence, a 50 Escudos coin must always be in the picture and selected by the user.

The algorithm seems to work alright, but it was quite a challenge for me to find a reliable distinction between 50 and 100 escudos that can be understood by a computer, even though they are easily distinguishable to the human eye. You can check out my code here on GitHub and I would very much appreciate suggestions for improvement.

## Demonstration Video

https://user-images.githubusercontent.com/61935581/210380336-f88f7874-460e-4ffd-adcb-bce202d60d64.mp4

## Acknowledgement

Many thanks to Nicholas Renotte and [his amazing video about 'action recognition' with Googles MediaPipe library](https://www.youtube.com/watch?v=doDUihpj6ro). Without this important inspiration, the project would not have been possible in this form.

## Installation

Clone the repository and create a new virtual environment

```bash
python3 -m venv envname # to create the virtual env
source envname/bin/activate # activate it
```

Afterwards install the libraries specified in requirements.txt

```bash
pip install -r requirements.txt
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
