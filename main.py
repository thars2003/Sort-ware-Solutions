import Computer_Vision.cleaned_result as cleaned_result
import Computer_Vision.rename_file as rename_file
import Computer_Vision.write_csv as write_csv



workplace="magiccolor"
parameter="Color"

write_csv.clear_csv(workplace)
write_csv.create_csv(parameter)

for i in range(1, 8): 
    name,color,colors = cleaned_result.clean_magiccolor(f"Scanned_Cards/test{i}.png", workplace)
    rename_file.rename_file(name, color, f"Scanned_Cards/test{i}.png")
    write_csv.append_csv(name,color)
