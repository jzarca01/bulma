# Bulma (Bullet Label Maker)

## Install dependencies
```pip install -r requirements.txt```

## How to use

In Photoshop, your psd file can use the following layer names:

- background
- beanName
- region
- country
- flavors
- process
- variety
- date

Then running the following command

```python main.py generate /home/pi/desktop/your_label.psd``` generates your_label.json that can be imported in Roast Time

```python main.py crop-front-label /home/pi/desktop/your_label.psd``` generates a png image file with the front label. Adapt the coordinates in the code.