for f in `ls *.ipynb`; do
    echo $f
    ipython nbconvert $f --to html
done
