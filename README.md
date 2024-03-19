# Installazione di Hadoop 3.2.0 in Windows Subsystem for Linux (WSL)

Questo tutorial ti guiderà attraverso i passaggi per installare Hadoop 3.2.0 in Windows Subsystem for Linux (WSL) e avviare una configurazione pseudo-distribuita (single-node mode). Questi passaggi sono pensati per essere eseguiti su un sistema Ubuntu WSL.

## Prerequisiti

Prima di iniziare, assicurati di aver installato Java JDK e di avere WSL configurato correttamente sul tuo sistema.

## 1. Installazione di Java JDK

Assicurati di avere Java JDK installato sul tuo sistema WSL. Puoi verificare la presenza di Java eseguendo il seguente comando:

```bash
java -version
```

Se Java non è installato, puoi installarlo tramite il seguente comando:
```bash
sudo apt-get install openjdk-8-jdk
```
2. Download del pacchetto binario Hadoop
Visita la pagina dei rilasci di Hadoop e trova il link per scaricare Hadoop 3.2.0. Ecco un esempio di URL per il download:
```bash
wget http://mirror.intergrid.com.au/apache/hadoop/common/hadoop-3.2.0/hadoop-3.2.0.tar.gz
```
3. Decomprimere il pacchetto binario Hadoop
Esegui il seguente comando per creare una cartella hadoop nella tua home directory e decomprimere il pacchetto binario:

```bash
mkdir ~/hadoop
tar -xvzf hadoop-3.2.0.tar.gz -C ~/hadoop
```

4. Configurazione della chiave SSH senza passphrase
Assicurati di poter effettuare il login SSH a localhost senza richiesta di passphrase. Esegui i seguenti comandi per generare le chiavi SSH:

```bash
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

5. Configurazione della modalità pseudo-distribuita (single-node mode)
Segui i seguenti passaggi per configurare Hadoop in modalità pseudo-distribuita:

5.1 Configurazione di JAVA_HOME
Modifica il file etc/hadoop/hadoop-env.sh e imposta la variabile JAVA_HOME:

```xml
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
```

5.2 Configurazione di core-site.xml
Modifica il file etc/hadoop/core-site.xml e aggiungi la seguente configurazione:

```xml
<configuration>
     <property>
         <name>fs.defaultFS</name>
         <value>hdfs://localhost:9000</value>
     </property>
</configuration>
```
5.3 Configurazione di hdfs-site.xml
Modifica il file etc/hadoop/hdfs-site.xml e aggiungi la seguente configurazione:

```xml
<configuration>
     <property>
         <name>dfs.replication</name>
         <value>1</value>
     </property>
</configuration>
```
5.4 Configurazione di mapred-site.xml
Modifica il file etc/hadoop/mapred-site.xml e aggiungi la seguente configurazione:

```xml
<configuration>
     <property>
         <name>mapreduce.framework.name</name>
         <value>yarn</value>
     </property>
     <property>
         <name>mapreduce.application.classpath</name>
         <value>$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/*:$HADOOP_MAPRED_HOME/share/hadoop/mapreduce/lib/*</value>
     </property>
</configuration>
```

5.5 Configurazione di yarn-site.xml
Modifica il file etc/hadoop/yarn-site.xml e aggiungi la seguente configurazione:

```xml
<configuration>
     <property>
         <name>yarn.nodemanager.aux-services</name>
         <value>mapreduce_shuffle</value>
     </property>
     <property>
         <name>yarn.nodemanager.env-whitelist</name>
         <value>JAVA_HOME,HADOOP_COMMON_HOME,HADOOP_HDFS_HOME,HADOOP_CONF_DIR,CLASSPATH_PREPEND_DISTCACHE,HADOOP_YARN_HOME,HADOOP_MAPRED_HOME</value>
     </property>
</configuration>
```
6. Formattazione del NameNode
Esegui il seguente comando per formattare il NameNode:

```bash
bin/hdfs namenode -format
```
7. Avvio dei servizi DFS
Esegui il seguente comando per avviare i servizi NameNode e DataNode:

```bash
sbin/start-dfs.sh
```
8. Avvio del servizio YARN
Esegui il seguente comando per avviare il servizio YARN:

```bash
sbin/start-yarn.sh
```
Ora dopo aver installato e configurato Hadoop 3.2.0 in modalità pseudo-distribuita sul tuo sistema WSL puoi accedere all' interfaccia hadoop tramite il seguente link: http://localhost:9870/explorer.html#/user

 9. Installazione di Apache Spark su Linux

Prima di tutto, dobbiamo scaricare il pacchetto binario di Apache Spark. Visita la pagina dei download sul sito web di Spark per trovare l'URL di download più vicino a te. Per esempio, il seguente URL è per il pacchetto Spark 2.4.3:

```bash
wget http://apache.mirror.serversaustralia.com.au/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.7.tgz
```

Una volta scaricato il pacchetto, possiamo decomprimerlo utilizzando il comando tar:

```bash
tar -xvzf spark-2.4.3-bin-hadoop2.7.tgz -C ~/hadoop
```
Ora è necessario configurare le variabili d'ambiente per Spark. Modifica il file .bashrc con il tuo editor preferito:

```bash
vi ~/.bashrc
```
Aggiungi le seguenti righe alla fine del file:

```bash
export SPARK_HOME=~/hadoop/spark-2.4.3-bin-hadoop2.7                                                                   
export PATH=$SPARK_HOME/bin:$PATH
```

Ricarica il file .bashrc per applicare le modifiche:

```bash

source  ~/.bashrc
```

Ora che abbiamo configurato Spark correttamente, possiamo verificare il corretto funzionamento eseguendo il seguente comando per avviare la shell interattiva di Spark:
```bash
spark-shell
```


10. Installazione e setup di Hive

Attingere dai link presenti nel seguente link per scegliere l'installazione più recente:
https://hive.apache.org/downloads.html

Nel terminale bash di WSL, esegui il seguente comando per scaricare il pacchetto:

```bash
wget http://www.strategylions.com.au/mirror/hive/hive-3.1.1/apache-hive-3.1.1-bin.tar.gz
```
Decomprimi il pacchetto binario
Se hai configurato Hadoop 3.2.0 con successo, dovrebbe esistere già una cartella hadoop nella tua home:

```bash
$ ls -lt
totale 611896
drwxrwxrwx 1 tangr tangr      4096 16 mag 00:32 dfs
drwxrwxrwx 1 tangr tangr      4096 15 mag 23:48 hadoop
-rw-rw-rw- 1 tangr tangr  345625475 22 gen 02:15 hadoop-3.2.0.tar.gz
-rw-rw-rw- 1 tangr tangr 280944629  1 nov  2018 apache-hive-3.1.1-bin.tar.gz
```
Ora decomprimi il pacchetto di Hive utilizzando il seguente comando:

```bash
tar -xvzf apache-hive-3.1.1-bin.tar.gz -C ~/hadoop
```
Nella cartella hadoop ci sono ora due sottocartelle:

```bash
$ ls ~/hadoop
apache-hive-3.1.1-bin  hadoop-3.2.0
```
Precedentemente abbiamo già configurato alcune variabili di ambiente come segue:

```bash
export JAVA_HOME=/usr/lib/jvm/java-1.8.0-openjdk-amd64
export HADOOP_HOME=/home/tangr/hadoop/hadoop-3.2.0
export PATH=$PATH:$HADOOP_HOME/bin
```
*Nota: il tuo nome utente può essere diverso.

Eseguiamo il seguente comando per aggiungere le variabili di ambiente richieste da Hive anche nel file .bashrc:

```bash
vi ~/.bashrc
```
Aggiungi le seguenti righe alla fine del file:

```bash
export HIVE_HOME=/home/tangr/hadoop/apache-hive-3.1.1-bin
export PATH=$HIVE_HOME/bin:$PATH
```
Cambia il nome utente con il tuo.

Esegui il seguente comando per rendere effettive le variabili:

```bash
source ~/.bashrc
```
Verifica le variabili di ambiente:

```bash
echo $HIVE_HOME
/home/tangr/hadoop/apache-hive-3.1.1-bin
```

Configura le cartelle HDFS di Hive
Avvia i tuoi servizi Hadoop (se non lo hai già fatto) eseguendo il seguente comando:

```bash
$HADOOP_HOME/sbin/start-all.sh
```

In WSL, potresti dover riavviare i servizi ssh se ssh non funziona e fornisce il seguente messaggio d'errore:

```bash
localhost: ssh: connect to host localhost port 22: Connection refused
```
Per riavviare i servizi, esegui il seguente comando:

```bash
sudo service ssh restart
```
Esegui il seguente comando (jps) per assicurarti che tutti i servizi siano in esecuzione con successo.

```bash
$ jps
2306 NameNode
2786 SecondaryNameNode
3235 NodeManager
3577 Jps
2491 DataNode
3039 ResourceManager
```
Se tutto sarà corretto il risultato del comando jps sarà di questo tipo.

Ora impostiamo le cartelle HDFS per Hive.

Esegui i seguenti comandi:

```bash
hadoop fs -mkdir /tmp 
hadoop fs -mkdir -p /user/hive/warehouse 
hadoop fs -chmod g+w /tmp 
hadoop fs -chmod g+w /user/hive/warehouse
```
Configura il metastore di Hive
Ora dobbiamo eseguire lo schematool per configurare il metastore per Hive. La sintassi del comando è la seguente:

```bash
$HIVE_HOME/bin/schematool -dbType <db type> -initSchema
```
Per l'argomento dbType, può essere uno dei seguenti valori:

```bash
derby|mysql|postgres|oracle|mssql
```
Per impostazione predefinita, verrà utilizzato Apache Derby. Tuttavia è un database standalone e può essere utilizzato solo per una connessione
contemporaneamente. Però per eseguire il codice all'interno di un istanza wsl è perfetto.


11.Abilitare il supporto di Hive
Se hai configurato Hive in WSL, segui i passaggi di seguito per abilitare il supporto di Hive in Spark. 

Copia i file di configurazione core-site.xml e hdfs-site.xml di Hadoop e hive-site.xml di Hive nella cartella di configurazione di Spark:
```bash
cp $HADOOP_HOME/etc/hadoop/core-site.xml $SPARK_HOME/conf/
cp $HADOOP_HOME/etc/hadoop/hdfs-site.xml $SPARK_HOME/conf/
cp $HIVE_HOME/conf/hive-site.xml $SPARK_HOME/conf/
```
La modifica di hive-site.xml sarà necessaria soltanto nel momento nel quale si vorrà utilizzare tutto questo sistema all'infuori della propria macchina locale.
Una volta faccio ciò si puotrà eseguire Spark con il supporto di Hive (funzione enableHiveSupport ed esempio di utilizzo):

```python
from pyspark.sql import SparkSession
nomeApplicazione = "Esempio Hive di PySpark"
master = "local[*]"
spark = SparkSession.builder \
             .appName(nomeApplicazione) \
             .master(master) \
             .enableHiveSupport() \
             .getOrCreate()
# Leggi i dati utilizzando Spark
df = spark.sql("show databases")
df.show()
```
