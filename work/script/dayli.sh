pip3 install -r requirements.txt
echo "requirements downloaded"
python3 download-dayli.py
echo "Files download end"
hadoop fs -put /work/data/* /data/
echo "Files pushed to hdfs"
rm -rf /work/data/* 