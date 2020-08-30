Htop
=========

Installs the new htop.

Requirements
------------

None.

Role Variables
--------------

Defaults:

htop_install_dir: "~/.local/bin/"
htop_version: "3.0.0"
htop_url: "https://github.com/htop-dev/htop/archive/{{ htop_version }}.tar.gz"
htop_checksum: "1c0661f0ae5f4e2874da250b60cd515e4ac4c041583221adfe95f10e18d1a4e6"

A description of the settable variables for this role should go here, including any variables that are in defaults/main.yml, vars/main.yml, and any variables that can/should be set via parameters to the role. Any variables that are read from other roles and/or the global scope (ie. hostvars, group vars, etc.) should be mentioned here as well.

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
        - role: htop
          tags: htop

License
-------

BSD
