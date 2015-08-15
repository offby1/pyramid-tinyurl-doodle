# -*- mode: ruby -*-

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network :forwarded_port, host: 6543, guest: 6543 # us
  config.vm.synced_folder ENV["HOME"], "/home/desktop"

  config.vm.provision "docker" do |d|
    #d.build_image "/vagrant/", args: "--tag offby1/tinyurl"
    d.pull_images "library/postgres"
    d.run "library/postgres",
          args: "--name db -v /var/lib/tinyurl-var-lib-postgresql-data:/var/lib/postgresql/data"
    d.run "tinyurl-prep",
          args: "--link db:db",
          image: "offby1/tinyurl",
          cmd: "initialize_tinyurl_db /tinyurl/production.ini",
          daemonize: false
    d.run "offby1/tinyurl",
          args: "-p 6543:80 --link db:db"
  end
end
