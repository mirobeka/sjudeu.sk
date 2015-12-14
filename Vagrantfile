# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.network "forwarded_port", guest: 80, host: 8080

  # install latest version of chef on machine
  # config.omnibus.chef_version = :latest

  config.vm.provision "chef_solo" do |chef|
      chef.cookbooks_path = ["cookbooks", "site-cookbooks"]

      chef.add_recipe "apt"
      chef.add_recipe "nginx"
      chef.add_recipe "rbenv::user"
      chef.add_recipe "rbenv::vagrant"

      # Install Ruby 2.2.1 and jekyll
      chef.json = {
        rbenv: {
          user_installs: [{
            user: 'vagrant',
            rubies: ["2.2.1"],
            global: "2.2.1",
            gems: {
              "2.2.1" => [
                { name: "jekyll" }
              ]
            }
          }]
        }
      }
  end
end
