# kali-build
## For toku's custom container images
This is my growing personal collection of tools I find useful from CTF events or tutorials I peruse. Since these don't have official binaries, or needed some kind of customization to work for my use-cases, I simply clone the repos down and add/update a Dockerfile to fit my needs.

Note that the structure of this is still very raw, as of this commit I am undecided as how I want to structure the files to make this a bit easier to consume; so consider this a backup in which I'm sharing a methodology rather than a repo to copy and use.

## Requirements
1. docker-cli
1. container runtime of your choosing
1. git

## Install
1. Clone into ~/.local/builds
1. Source ./aliases from favorite profile configuration
1. `upgradecontainers`

## Use
You can assume that, if the binary requires files to input/output, they will usually either be mounted in the working directory of the container or in `target/$(current_directory)` so they can be used as if actually a binary, or prepending `target/` to the file. The entrypoint will (hopefully) always be the built artifact from the repo, so simply follow the repos instructions to use and cross your fingers.

### Example 1 with target/file:
```sh
[09:21:39] tokugero :: pangolin  ➜  pwn/rocketblasterxxx/challenge » ropper -f target/rocket_blaster_xxx | grep "rdi"                                                                                                                   1 ↵
0x0000000000401359: add byte ptr [rax - 0x77], cl; ror dword ptr [rax - 0x73], 5; movsb byte ptr [rdi], byte ptr [rsi]; or al, 0; add byte ptr [rax - 0x77], cl; ret 0x8d48; 
0x0000000000401578: add byte ptr [rax], al; mov rdi, rax; call 0x10e0; mov eax, 0; leave; ret; 
0x00000000004014ba: add byte ptr [rax], al; mov rdi, rax; call 0x1140; nop; leave; ret; 
0x00000000004014b7: add eax, 0x3b54; mov rdi, rax; call 0x1140; nop; leave; ret; 
0x00000000004014b6: mov eax, dword ptr [rip + 0x3b54]; mov rdi, rax; call 0x1140; nop; leave; ret; 
0x00000000004014b5: mov rax, qword ptr [rip + 0x3b54]; mov rdi, rax; call 0x1140; nop; leave; ret; 
0x000000000040157a: mov rdi, rax; call 0x10e0; mov eax, 0; leave; ret; 
0x00000000004014bc: mov rdi, rax; call 0x1140; nop; leave; ret; 
0x00000000004012e5: mov rdi, rax; mov eax, 0; call 0x10f0; nop; pop rbp; ret; 
0x00000000004012a8: mov rdi, rax; mov eax, 0; call 0x10f0; nop; leave; ret; 
0x0000000000401360: movsb byte ptr [rdi], byte ptr [rsi]; or al, 0; add byte ptr [rax - 0x77], cl; ret 0x8d48; 
0x00000000004011e6: or dword ptr [rdi + 0x405010], edi; jmp rax; 
0x000000000040159f: pop rdi; ret; 
0x000000000040135c: ror dword ptr [rax - 0x73], 5; movsb byte ptr [rdi], byte ptr [rsi]; or al, 0; add byte ptr [rax - 0x77], cl; ret 0x8d48; 
```

### Example 2 with just file:
```sh
[09:37:58] tokugero :: pangolin  ➜  apocalypse2024/forensics/pursuethetracks » mft z.mft | head -10
{
  "header": {
    "signature": [
      70,
      73,
      76,
      69
    ],
    "usa_offset": 48,
    "usa_size": 3,
```