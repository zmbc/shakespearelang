# pexpect helpers
def expect_interaction(cli, to_send, to_receive, prompt=True):
    cli.sendline(to_send)
    full_output = ""
    if to_receive:
        full_output = to_receive + "\n"
    if prompt:
        full_output = full_output + ">> "
    expect_output_exactly(cli, full_output)


def expect_output_exactly(cli, output, eof=False):
    output = output.replace("\n", "\r\n")
    output_index = 0
    while output_index < len(output):
        output_received = cli.read_nonblocking(len(output) - output_index).decode(
            "utf-8"
        )
        expected_output_batch = output[
            output_index : (output_index + len(output_received))
        ]
        assert output_received == expected_output_batch
        output_index = output_index + len(output_received)

    if eof:
        assert cli.read().decode("utf-8") == ""

def create_play_file(path, contents):
    with open(path, "w") as f:
        f.write(contents)
