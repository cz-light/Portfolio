#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>
#include <stdbool.h>

void handler(int sig) {
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int isInputRedirection(char **tokens, int token_count){
    for (int i = 0; i < token_count; i++){
        if (strcmp(tokens[i],"<")==0){
            return i;
        }
    }
    return -1;
    
}

int isOutputRedirection(char **tokens, int token_count){
    for (int i = 0; i < token_count; i++){
        if (strcmp(tokens[i],">")==0){
            return i;
        }
    }
    return -1;
}

bool isBackground(char **tokens, int token_count){
    if (strcmp(tokens[token_count-1],"&")==0){
        return true;
    }
    return false;
}




int main(){
    signal(SIGCHLD, handler);

    char currentpath[100];
    getcwd(currentpath, sizeof(currentpath));

    char input[50];
    int end = 0;

    while (end < 1){
        printf("%s> ", currentpath);
        //fgets creatse a newline at the end of input-- it needs to be removed so it can be compared to later strings
        fgets(input,sizeof(input),stdin);
        input[strcspn(input, "\n")] = 0;

        //tokenize input (can be a function)
        char *tokenized[50];
        char *token = strtok(input, " ");
        int token_count = 0;
        while (token != NULL){
            tokenized[token_count] = token;
            token_count++;
            token = strtok(NULL, " ");     
        }
        tokenized[token_count] = NULL;
        if (strcmp(tokenized[0],"exit")==0){
            end = 1;
        }

        //deal with input and output redirection (output of functions are index of token with < or >)
        //the output is used in child process after the fork
        int inputRedirection = isInputRedirection(tokenized, token_count);
        int outputRedirection = isOutputRedirection(tokenized, token_count);

        //deal with background processing
        bool background = isBackground(tokenized, token_count);
        if (background){
            tokenized[token_count-1] = NULL;
        }
        
       
        //logic for commands starts here
        if (token_count>0 && strcmp(tokenized[0],"cd")==0){
            int changeDirectory = chdir(tokenized[1]);
            if (changeDirectory == 0){
                getcwd(currentpath, sizeof(currentpath));
            }
            else{
                printf("Error: No such directory\n");
            }

        }
        //else if (token_count>0 && (strcmp(tokenized[0],"ls")==0 || strcmp(tokenized[0],"ps") ==0)){
        else if (token_count>0){
            //followed from the forkwaitexample.c on canvas
            int pid = fork();
            
            //deal with redirection
            if (pid == 0){
                if (inputRedirection!=-1){
                    freopen(tokenized[inputRedirection+1], "r", stdin);
                    tokenized[inputRedirection] = NULL;
                    tokenized[inputRedirection+1] = NULL;
                }
                if (outputRedirection!=-1){
                    freopen(tokenized[outputRedirection+1], "w", stdout);
                    tokenized[outputRedirection] = NULL;
                    tokenized[outputRedirection+1] = NULL;
                }       

                //child process
                execvp(tokenized[0], tokenized);
                printf("Error: Command not found\n");

            } else {
                int status;
                //blocking wait so the output is in order
                if (!background){
                    int result = waitpid(pid, &status, 0);                
                }
            }
        }
        else if (token_count>0){
            printf("Error: Command not found\n");}
    }

    printf("Exiting shell...\n");


    return 0;
}