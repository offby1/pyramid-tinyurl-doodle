# -*- mode: ruby -*-

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "trusty64"
  config.vm.network :forwarded_port, host: 5432, guest: 5432 # postgres
  config.vm.network :forwarded_port, host: 6543, guest: 6543 # us

  # Crude by-hand deployment instructions:
  # apt-get install postgresql
  # su - postgres
  # createuser -DRS vagrant ; createdb -O vagrant vagrantwork ; exit
  # apt-get build-dep python-psycopg2
end
