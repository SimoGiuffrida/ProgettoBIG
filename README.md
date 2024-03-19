# Installazione di Hadoop 3.2.0 in Windows Subsystem for Linux (WSL)

Questo tutorial ti guiderà attraverso i passaggi per installare Hadoop 3.2.0 in Windows Subsystem for Linux (WSL) e avviare una configurazione pseudo-distribuita (single-node mode). Questi passaggi sono pensati per essere eseguiti su un sistema Ubuntu WSL.

## Prerequisiti

Prima di iniziare, assicurati di aver installato Java JDK e di avere WSL configurato correttamente sul tuo sistema.

## 1. Installazione di Java JDK

Assicurati di avere Java JDK installato sul tuo sistema WSL. Puoi verificare la presenza di Java eseguendo il seguente comando:

```bash
java -version
Se Java non è installato, puoi installarlo tramite il seguente comando:
```
```bash
sudo apt-get install openjdk-8-jdk
```
2. Download del pacchetto binario Hadoop
Visita la pagina dei rilasci di Hadoop e trova il link per scaricare Hadoop 3.2.0. Ecco un esempio di URL per il download:
```bash
Copy code
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
Ora hai installato e configurato Hadoop 3.2.0 in modalità pseudo-distribuita sul tuo sistema WSL. Puoi accedere alle interfacce web dei servizi NameNode e ResourceManager tramite i seguenti URL:

NameNode
ResourceManager
