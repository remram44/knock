��          �   %   �      p  0   q  1   �  
   �  C   �  @   #     d          �     �  3   �     �  &        @  &   _     �  &   �     �  %   �          "  #   <     `  V  g     �     �     �      �  �  �  ;   �	  =   �	      
  X   
  V   i
  "   �
  "   �
  %     	   ,  3   6      j  *   �      �  *   �        *   #     N  /   a  !   �  $   �  (   �       �       �     �     �  .   �                       	                                                                   
                                 
Results for ports scanned on the local machine: 
Results for ports scanned on the remote machine: (selected) Couldn't guess local hostname from SSH environment -- please use -l Couldn't guess remote hostname from SSH command -- please use -r Couldn't lookup {hostname} Couldn't setup the Python path
 Couldn't start the ssh process Error:  Hostname {hostname} resolved to multiple addresses: Option -l requires an argument Option -l was specified more than once Option -r requires an argument Option -r was specified more than once Option -s requires an argument Option -s was specified more than once Port        Status Port sequence goes backwards: {0}-{1} Port spec couldn't be parsed Server exited prematurely Total: {open} open, {closed} closed closed knock [options] [ports] [...] [user@host] [/usr/bin/python path/to/knock]

  Tests for port accessibility between here and the remote machine.

  Ports can have the format '42' or '41-47'; a '-' prefix means to test the
local port from the remote side.

Recognized options:
  -h
    Prints this help and exits
  -s <ssh_cmd>
    Sets the SSH binary (default: 'ssh')
  -r <hostname>
    Sets the hostname or address of the remote machine that we'll use to test
    remote ports
  -l <hostname>
    Sets the hostname or address of this machine that will be used by the
    remote to test local ports
 local error open remote skipped ssh arguments were not specified Project-Id-Version: 0.1
Report-Msgid-Bugs-To: remirampin@gmail.com
POT-Creation-Date: 2014-04-22 23:16-0400
PO-Revision-Date: 2014-04-22 23:18-0500
Last-Translator: Remi Rampin <remirampin@gmail.com>
Language-Team: 
Language: fr_FR
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=2; plural=(n > 1);
X-Generator: Poedit 1.5.7
 
Résultats pour les ports scannés sur la machine locale : 
Résultats pour les ports scannés sur la machine distante : (sélectionné) Impossible de deviner l'adresse locale depuis l'environnement SSH -- merci
d'utiliser -l Impossible de deviner l'adresse distante depuis la commande SSH -- merci
d'utiliser -r Impossible de résoudre {hostname} N'a pas pu régler le path Python
 Impossible de lancer le programme ssh Erreur :  Le nom {hostname} a résolu en plusieurs adresses : L'option -l requiert un argument L'option -l a été passée plusieurs fois L'option -r requiert un argument L'option -r a été passée plusieurs fois L'option -s requiert un argument L'option -s a été passée plusieurs fois Port        Statut La séquence de ports est à l'envers : {0}-{1} Les ports n'ont pas été compris Le serveur a quitté prématurément Total : {open} ouverts, {closed} fermés fermé knock [options] [ports] [...] [user@host] [/usr/bin/python chemin/vers/knock]

  Teste l'accessibilité des ports entre ici et la machine distante.

  Les ports peuvent avoir le format '42' ou '41-47'; un prefix '-' indique de
tester le port local depuis la machine distante.

Options reconnues :
  -h
    Affiche cette aide et termine
  -s <ssh_cmd>
    Change le binaire SSH (par défaut : 'ssh')
  -r <nom d'hôte>
    Définit le nom de domaine ou l'adresse de la machine distante qui sera
    utilisé pour tester les ports distants
  -l <nom d'hôte>
    Définit le nom de domaine ou l'adresse de cette machine qui sera utilisé
    par la machine distante pour tester les ports locaux
 erreur locale ouvert sauté par le serveur Les arguments de ssh n'ont pas été indiqués 