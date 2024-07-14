<#
Download ISOs of Windows 10, Windows 11, and Windows Server 2022 if they do not exist
in the directory where I typically store ISOs.
#>
$Windows10ISO = "C:\Users\Brandon\ISOs\Win10_22H2_English_x64v1.iso"
$WindowsServer2022ISO = "C:\Users\Brandon\ISOs\en-us_windows_server_2022_updated_june_2024_x64_dvd_8c5a802d.iso"

Write-Output "`n** Checking for both Windows 10 and Windows Server ISOs in C:\Users\Brandon\ISOs"
if ((Test-Path $Windows10ISO) -and (Test-Path $WindowsServer2022ISO)) {
    Write-Output "`n** Found both ISOs"
} else {
    # download Windows 10 ISO and store it in the typical path locatin
    Write-Output "`n** Downloading Windows 10 ISO"
    Invoke-WebRequest https://drive.massgrave.dev/en-us_windows_10_consumer_editions_version_22h2_updated_june_2024_x64_dvd_a8751094.iso $Windows10ISO
    Write-Output "`n** Stored Windows 10 ISO at $($Windows10ISO)"

    # download Windows Server 2022 ISO and store it in the typical path locatin
    Write-Output "`n** Downloading Windows Server 2022 ISO"
    Invoke-WebRequest https://drive.massgrave.dev/en-us_windows_server_2022_updated_june_2024_x64_dvd_8c5a802d.iso $WindowsServer2022ISO
    Write-Output "`n** Stored Windows Server 2022 ISO at $($WindowsServer2022ISO)"
}

<#
Create VMs for both Windows 10 and Windows Server 2022.
Update this to take in command line parameters for the size and shit, maybe later.
#>
$Windows10VMName = "Windows 10 (Client)"
$Windows10VMType = "Windows10_64"
Write-Output "`n** Creating Windows 10 VM"
VBoxManage.exe createvm --name $Windows10VMName --ostype $Windows10VMType --register
VBoxManage.exe createhd --filename "C:\Users\Brandon\VirtualBox VMs\$Windows10VMName\$Windows10VMName.vdi" --size 50000 --format VDI --variant Standard
VBoxManage.exe storagectl $Windows10VMName --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage.exe storageattach $Windows10VMName --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "C:\Users\Brandon\VirtualBox VMs\$Windows10VMName\$Windows10VMName.vdi"
VBoxManage.exe modifyvm $Windows10VMName --memory 8196 --graphicscontroller VBoxSVGA --vram 256 --accelerate3d on --cpus 4
VBoxManage.exe modifyvm $Windows10VMName --boot1 dvd --boot2 disk --boot3 none --boot4 none
VBoxManage.exe modifyvm $Windows10VMName --clipboard bidirectional --draganddrop bidirectional
VBoxManage.exe modifyvm $Windows10VMName --nic1 intnet
VBoxManage.exe storagectl $Windows10VMName --name "IDE Controller" --add ide
VBoxManage.exe storageattach $Windows10VMName --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium $WindowsServer2022ISO
Write-Output "** Successfully created Windows 10 VM"
VBoxManage.exe startvm $Windows10VMName

$WindowsServer2022VMName = "Windows Server 2022 (Server)"
$WindowsServer2022VMType = "Windows2022_64"
Write-Output "`n** Creating Windows Server 2022 VM"
VBoxManage.exe createvm --name $WindowsServer2022VMName --ostype $WindowsServer2022VMType --register
VBoxManage.exe createhd --filename "C:\Users\Brandon\VirtualBox VMs\$WindowsServer2022VMName\$WindowsServer2022VMName.vdi" --size 50000 --format VDI --variant Standard
VBoxManage.exe storagectl $WindowsServer2022VMName --name "SATA Controller" --add sata --controller IntelAhci
VBoxManage.exe storageattach $WindowsServer2022VMName --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium "C:\Users\Brandon\VirtualBox VMs\$WindowsServer2022VMName\$WindowsServer2022VMName.vdi"
VBoxManage.exe modifyvm $WindowsServer2022VMName --memory 8196 --graphicscontroller VBoxSVGA --vram 256 --accelerate3d on --cpus 4
VBoxManage.exe modifyvm $WindowsServer2022VMName --boot1 dvd --boot2 disk --boot3 none --boot4 none
VBoxManage.exe modifyvm $WindowsServer2022VMName --clipboard bidirectional --draganddrop bidirectional
VBoxManage.exe modifyvm $WindowsServer2022VMName --nic1 intnet
VBoxManage.exe modifyvm $WindowsServer2022VMName --nic1 nat
VBoxManage.exe storagectl $WindowsServer2022VMName --name "IDE Controller" --add ide
VBoxManage.exe storageattach $WindowsServer2022VMName --storagectl "IDE Controller" --port 0 --device 0 --type dvddrive --medium $WindowsServer2022ISO
Write-Output "** Successfully created Windows Server 2022 VM"
VBoxManage.exe startvm $WindowsServer2022VMName