# NOTE: This Dockerfile is provided for reference ONLY.
# It is NOT the production Dockerfile used for the challenge.
# The sole purpose here is to reveal the system environment
# that the challenge is being hosted in.
#
# In other words the most important clause is the FROM clause.
# sshd
#
# VERSION               0.0.2

FROM mcr.microsoft.com/dotnet/core/sdk:3.0

RUN useradd -u 1234 -m demo
ADD pwn2.csproj /home/demo
ADD Program.cs /home/demo
ADD flag.txt /home/demo
RUN cd /home/demo && dotnet build -c Release
WORKDIR /home/demo


EXPOSE 9998
EXPOSE 9999
RUN apt-get update && apt-get install -y gdbserver socat
CMD socat TCP-LISTEN:9998 EXEC:"gdbserver \:9999 bin/Release/netcoreapp3.0/pwn2"
# CMD ["/bin/bash"]
# CMD ["gdbserver", ":9999", "--attach","$(pgrep -f pwn2)"]
