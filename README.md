# High performance stack #

## Requirements ##

 - Install `vagrant` (https://www.vagrantup.com/downloads.html)
 - Add `vagrant` command to `PATH` variable (if need)

## WorkFlow ##

    vagrant up  # starts and provisions the vagrant environment
    vagrant ssh  # connects to machine via SSH
    
    vagrant destroy  # stops and deletes all traces of the vagrant machine

## imm.py ##

Simple automation tool for compiling and running your programs on 
IMM URAN supercomputer.

Also, you can use it for local running. 

 1. Setup you environment

        def local_env():
            env.user = 'vagrant'
            env.password = 'vagrant'
            env.host_string = 'localhost:22'
        
        
        def cluster_env():
            env.user = 's0*****'
            env.password = 'Vjk******'
            env.host_string = 'umt.imm.uran.ru:22'

 2. Write your compiling and running commands

        def main():
            # put files to remote server
            _put('kmeans.cpp')  
            _put('data-gen.cpp')
            
            # compiling command && run
            run('g++ data-gen.cpp -o data-gen && ./data-gen 3 10 10 data-gen.txt')
            run('g++ kmeans.cpp -o kmeans -fopenmp && ./kmeans 10 data-gen.txt kmeans.txt')
            
            # get files from remote server
            _get('data-gen.txt')
            _get('kmeans.txt')
            
        if __name__ == "__main__":
            local_env()  # activate local environment
            #supercomputer_env()  # or activate supercomputer environment
            main()  # running main :) 

 3. Up container (`vagrant up`)

 4. Connect via SSH to container (`vagrant ssh`)

 5. Run `imm.py` (`python imm.py`)

 6. Check you result
