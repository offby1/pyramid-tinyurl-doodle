# -*- mode: ruby -*-

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.box = "ubuntu/trusty64"

  # A privately whipped-up variant of the above, but with an updated
  # 'vboxguest' module.  Starting this box up is faster than the
  # above, since it doesn't have to update that guest.  (If the above
  # doesn't update the guest, I expect that the synced folders won't work.)
  config.vm.box = "trusty64-updated-vboxguest"

  config.vm.network :forwarded_port, host: 6543, guest: 6543 # us
  config.vm.synced_folder ENV["HOME"], "/home/desktop"

  config.vm.provider "virtualbox" do |v|
    v.memory = 1024
  end

  config.vm.provision "docker" do |d|
    #d.build_image "/vagrant/", args: "--tag offby1/tinyurl"

    d.run "offby1/tinyurl",
          args: "--name tinyurl -p 6543:80"
  end
end
