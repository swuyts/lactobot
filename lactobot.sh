pin=/home/pi/lactobot

cd $pin
echo DOWNLOADING NCBI DATABASE
echo 
cd ncbi_files/
wget "ftp://ftp.ncbi.nlm.nih.gov/genomes/genbank/bacteria/assembly_summary.txt"

echo EXTRACTING LACTOBACILLUS
echo
grep "Lactobacillus" assembly_summary.txt > lactos.txt

rm -f assembly_summary.txt
cd $pin

echo EXECUTING PYTHON SCRIPT
echo
python tweet.py
